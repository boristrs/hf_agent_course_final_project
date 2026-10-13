import time
from typing import Any
import requests

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import BaseTool, tool

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


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


@tool
def fetch_page(url: str) -> str:
    """Fetch the full content of a web page.
    MUST be used if the question contains a web page to search for or if the search tool resulted in web pages that would be needed to explore to get the relevant information.
    Args:
        url (str): The URL of the page to fetch.
    Returns:
        str: The text content of the page (first 15000 characters).
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        if HAS_BS4:
            soup = BeautifulSoup(response.text, 'html.parser')
            for element in soup(['script', 'style', 'nav', 'footer', 'head', 'iframe']):
                element.decompose()
            text = soup.get_text(separator='\n', strip=True)
            text = '\n'.join(line for line in text.splitlines() if line)
            return f"Content from {url}:\n\n{text[:15000]}"
        else:
            return f"Content from {url}:\n\n{response.text[:15000]}"
    except requests.RequestException as e:
        return f"Failed to fetch page: {e}"
    except Exception as e:
        return f"Error processing page: {e}"
