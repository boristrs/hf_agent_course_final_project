import time
from typing import Any

from langchain_community.tools import DuckDuckGoSearchResults, DuckDuckGoSearchRun
from langchain_core.tools import BaseTool, tool


_news_search = DuckDuckGoSearchResults(output_format="list", num_results=5)
_web_search = DuckDuckGoSearchRun()


class SearchUnavailableError(RuntimeError):
    pass


def _invoke_with_retry(search: BaseTool, query: str) -> Any:
    for attempt in range(3):
        try:
            return search.invoke(query)
        except Exception as exc:
            if attempt == 2:
                raise SearchUnavailableError(
                    f"DuckDuckGo search failed after 3 attempts "
                    f"({type(exc).__name__}: {exc})"
                ) from exc
            time.sleep(2**attempt)


@tool
def get_latest_news(topic: str) -> str:
    """Search for recent news articles about a topic, including headlines and links."""
    if not topic.strip():
        raise ValueError("topic must not be empty")

    try:
        articles = _invoke_with_retry(_news_search, f"latest news about {topic}")
    except SearchUnavailableError as exc:
        return str(exc)

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


@tool
def search_tool(query: str) -> str:
    """Search the web for information relevant to a query."""
    try:
        return _invoke_with_retry(_web_search, query)
    except SearchUnavailableError as exc:
        return str(exc)
