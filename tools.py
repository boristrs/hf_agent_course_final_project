from langchain_community.tools import DuckDuckGoSearchResults, DuckDuckGoSearchRun
from langchain_core.tools import tool

from huggingface_hub import list_models

import random

_news_search = DuckDuckGoSearchResults(output_format="list", num_results=5)

@tool
def get_latest_news(topic: str) -> str:
    """Search for recent news articles about a topic, including headlines and links."""
    if not topic.strip():
        raise ValueError("topic must not be empty")

    articles = _news_search.invoke(f"latest news about {topic}")
    if not articles:
        return f"No recent news articles found for {topic!r}."

    formatted_articles = []
    for article in articles:
        title = article.get("title", "Untitled")
        snippet = article.get("snippet", "")
        url = article.get("link", "")
        formatted_articles.append(
            f"Headline: {title}\n"
            f"Summary: {snippet}\n"
            f"Link: {url}"
        )

    return "\n\n".join(formatted_articles)

from langchain_community.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()
