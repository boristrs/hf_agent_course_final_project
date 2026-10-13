from langchain_core.tools import tool

from youtube_transcript_api import YouTubeTranscriptApi



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