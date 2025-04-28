from typing import Any, Dict

from news_navigator.app.tools import get_news
from news_navigator.app.graph import create_news_agent_graph


class NewsAgent:
    """News agent that retrieves and summarizes news articles."""

    def __init__(self, model_name="gpt-4o"):
        """Initialize the news agent with tools and model."""
        self.tools = [get_news]
        self.graph = create_news_agent_graph(self.tools, model_name)

    def search(self, query: str) -> Dict[str, Any]:
        """
        Search for news articles based on the provided query.

        Args:
            query: The topic or search query for news articles

        Returns:
            Dict containing a summary and top 10 articles with references
        """
        # Invoke the graph
        result = self.graph.invoke(
            {
                "query": query,
                "raw_articles": [],
                "summarized_results": "",
                "top_articles": [],
            }
        )

        return {
            "summary": result["summarized_results"],
            "articles": result["top_articles"],
        }

    def format_results(self, results: Dict[str, Any]) -> str:
        """Format the results for display."""
        output = "# News Summary\n\n"
        output += results["summary"]

        output += "\n\n# Top 10 Recent Articles\n\n"

        for i, article in enumerate(results["articles"], 1):
            output += f"{i}. [{article['title']}]({article['url']})\n"
            output += f"   Source: {article['source']}\n"
            output += f"   Published: {article['published_at']}\n\n"

        return output
