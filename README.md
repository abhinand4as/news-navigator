# News Navigator

News Navigator is a LangGraph-powered agent that retrieves and summarizes the latest news about any topic. Simply provide a search query, and the agent will fetch recent articles, generate a comprehensive summary, and provide links to the top 10 most relevant stories.

## Features

- 🔍 Search for news on any topic
- 📊 Get a comprehensive summary of current coverage
- 🔗 Access links to the top 10 most recent and relevant articles
- 🧠 Uses LLM-powered summarization for high-quality results
- 🛠️ Built with LangGraph for a modular, maintainable architecture

## Installation

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- News API key (get one from [newsapi.org](https://newsapi.org/))
- OpenAI API key

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/news-navigator.git
   cd news-navigator
   ```

2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

3. Create a `.env` file in the project root with your API keys:
   ```
   NEWS_API_KEY=your_news_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Command Line

Run News Navigator with a search query:

```bash
poetry run news-navigator "artificial intelligence"
```

Or use the Python module directly:

```bash
poetry run python -m news_navigator.main "climate change"
```

## Project Structure

```
news_navigator/
├── app/
│   ├── __init__.py
│   ├── agent.py          # Main agent implementation
│   ├── tools/
│   │   ├── __init__.py
│   │   └── news_tool.py  # News API tool
│   └── graph/
│       ├── __init__.py
│       └── workflow.py   # State graph definition
└── main.py               # Entry point for the application
```

## How It Works

News Navigator uses a LangGraph workflow with three main steps:

1. **Query Processing**: Takes the user's search query and prepares it for news retrieval
2. **News Fetching**: Calls the News API to retrieve recent articles about the topic
3. **Summarization**: Uses OpenAI's language models to create a comprehensive summary of the news coverage

## Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Uses [NewsAPI](https://newsapi.org/) for article retrieval
- Powered by [OpenAI](https://openai.com/) language models

---

Created with ❤️ using AI-powered development tools