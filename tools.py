import time
from typing import Any

from langchain_community.tools import DuckDuckGoSearchResults, DuckDuckGoSearchRun
from langchain_core.tools import BaseTool, tool

from youtube_transcript_api import YouTubeTranscriptApi


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
def inspect_video_frames(video_url: str) -> str:
    """Inspect the frames of a video and return a summary of the content.
    Args:
        video_url (str): The URL of the video to inspect.
    Returns:
        str: A summary of the video content.
    """
    # Placeholder implementation - replace with actual video frame inspection logic
    return f"Inspecting video frames for {video_url}"

@tool
def get_youtube_transcript(video_url: str, languages: list[str] = ["en"]) -> str:
    """Get the transcript of a YouTube video.
    Args:
        video_url (str): The URL of the YouTube video.
        languages (list[str]): The languages to fetch transcripts for. If not known, defaults to English.
    Returns:
        str: The transcript of the video.
    """
    video_id = video_url.split("v=")[-1]
    transcript = YouTubeTranscriptApi().fetch(
    video_id,
    languages=languages,
    )
    text = "\n".join(segment.text for segment in transcript)
    print(f"Retrieving transcript for {video_url}")
    # Placeholder implementation - replace with actual YouTube transcript retrieval logic
    return text