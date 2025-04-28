import os
import sys

from news_navigator.app.agent import NewsAgent
from dotenv import load_dotenv


def main():
    """
    Main entry point for the news agent application.
    Run this file to search for news about a specific topic.

    Usage:
        python main.py <search query>

    Example:
        python main.py "artificial intelligence"
    """
    load_dotenv()  # Load environment variables

    # Check if NEWS_API_KEY is set
    if not os.getenv("NEWS_API_KEY"):
        print("Error: NEWS_API_KEY environment variable not set.")
        print(
            "Please obtain an API key from https://newsapi.org/ and set it in your .env file."
        )
        sys.exit(1)

    # Check if OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key in your .env file.")
        sys.exit(1)

    # Get query from command line arguments
    if len(sys.argv) < 2:
        print("Please provide a search query.")
        print('Usage: python main.py "your search query"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    print(f"Searching for news about: {query}")
    print("This may take a moment...")

    # Initialize the agent
    agent = NewsAgent()

    try:
        # Search for news
        results = agent.search(query)

        # Format and display results
        formatted_results = agent.format_results(results)
        print("\n" + formatted_results)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
