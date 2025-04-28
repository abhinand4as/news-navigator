from typing import Any, Dict, List, TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph


class NewsAgentState(TypedDict):
    """State for the news agent."""

    query: str  # User's search query
    raw_articles: List[Dict]  # Raw articles from the news API
    summarized_results: str  # Summary of the news results
    top_articles: List[Dict]  # Top 10 articles with references


def create_news_agent_graph(tools, model_name="gpt-4o"):
    """Create a news agent graph with the provided tools."""

    # Node to extract query
    def query_node(state: NewsAgentState) -> Dict:
        """Process the input query."""
        # The query is already in the state
        return {"next": "fetch_news"}

    # Node to fetch news
    def fetch_news_node(state: NewsAgentState) -> Dict:
        """Fetch news articles using the news tool."""
        query = state["query"]
        get_news_tool = next(tool for tool in tools if tool.name == "get_news")

        try:
            articles = get_news_tool.invoke(query)
            return {"raw_articles": articles, "next": "summarize_news"}
        except Exception as e:
            return {
                "raw_articles": [],
                "summarized_results": f"Error fetching news: {str(e)}",
                "next": END,
            }

    # Node to summarize news
    def summarize_news_node(state: NewsAgentState) -> Dict:
        """Summarize the news articles using an LLM."""
        articles = state["raw_articles"]
        query = state["query"]

        if not articles:
            return {
                "summarized_results": f"No news articles found for '{query}'.",
                "top_articles": [],
                "next": END,
            }

        llm = ChatOpenAI(model=model_name)

        # Prepare context for the LLM
        context = f"Here are {len(articles)} news articles about '{query}':\n\n"

        for i, article in enumerate(articles):
            context += f"{i+1}. Title: {article['title']}\n"
            context += f"   Description: {article['description']}\n"
            context += f"   Source: {article['source']}\n"
            context += f"   Published: {article['published_at']}\n\n"

        prompt = f"""
        Based on the following news articles about '{query}', provide:
        
        1. A comprehensive summary of the overall news coverage (about 2-3 paragraphs)
        2. Key points or trends in the news
        
        Context:
        {context}
        """

        # Get the summary from the LLM
        response = llm.invoke(prompt)
        summary = response.content

        # Format the top articles with references
        top_articles = []
        for article in articles:
            top_articles.append(
                {
                    "title": article["title"],
                    "source": article["source"],
                    "url": article["url"],
                    "published_at": article["published_at"],
                }
            )

        return {
            "summarized_results": summary,
            "top_articles": top_articles,
            "next": END,
        }

    # Create the graph
    workflow = StateGraph(NewsAgentState)

    # Add nodes
    workflow.add_node("input_query", query_node)
    workflow.add_node("fetch_news", fetch_news_node)
    workflow.add_node("summarize_news", summarize_news_node)

    # Add edges
    workflow.add_conditional_edges(
        "input_query", lambda x: x.get("next"), {"fetch_news": "fetch_news", END: END}
    )

    workflow.add_conditional_edges(
        "fetch_news",
        lambda x: x.get("next"),
        {"summarize_news": "summarize_news", END: END},
    )

    workflow.add_conditional_edges(
        "summarize_news", lambda x: x.get("next"), {END: END}
    )

    # Set entry point
    workflow.set_entry_point("input_query")

    return workflow.compile()
