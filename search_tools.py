import time
from typing import Any

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import BaseTool, tool


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
def search_tool(query: str) -> str:
    """Search the web for information relevant to a query.
    Args:
        query (str): The search query.
    Returns:
        str: The search results.
    """
    try:
        return _invoke_with_retry(_web_search, query)
    except SearchUnavailableError as exc:
        return str(exc)
