import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


class NewsAPIException(Exception):
    """Exception raised for errors in the News API."""

    pass


@tool
def get_news(query: str) -> List[Dict[str, Any]]:
    """
    Get the latest news articles about a specific topic or query.

    Args:
        query: The topic or search query for news articles

    Returns:
        A list of dictionaries containing news articles with title, description, url,
        source, author, and published date
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        raise NewsAPIException("NEWS_API_KEY not found in environment variables")

    # Calculate date one week ago for recent news
    one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # Construct API URL
    base_url = "https://newsapi.org/v2/everything"

    # Parameters for the API request
    params: Dict[str, Union[str, int]]= {
        "q": query,
        "from": one_week_ago,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": api_key,
        "pageSize": 10,  # Get top 10 results
    }

    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()

        if data["status"] != "ok":
            raise NewsAPIException(f"API Error: {data.get('message', 'Unknown error')}")

        articles = data.get("articles", [])

        # Format the articles
        formatted_articles = []
        for article in articles:
            formatted_articles.append(
                {
                    "title": article.get("title", "No title"),
                    "description": article.get("description", "No description"),
                    "url": article.get("url", ""),
                    "source": article.get("source", {}).get("name", "Unknown source"),
                    "author": article.get("author", "Unknown author"),
                    "published_at": article.get("publishedAt", ""),
                }
            )

        return formatted_articles

    except requests.exceptions.RequestException as e:
        raise NewsAPIException(f"Request Error: {str(e)}")
    except Exception as e:
        raise NewsAPIException(f"Error retrieving news: {str(e)}")
