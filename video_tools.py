# import cv2
import numpy as np
from io import BytesIO
import requests
from langchain_core.tools import tool
from typing import Optional
import tempfile
import os

from youtube_transcript_api import YouTubeTranscriptApi


# def _download_video_from_url(url: str, max_size_mb: int = 50) -> Optional[str]:
#     """Download video from URL to a temporary file. Returns local path or None."""
#     try:
#         response = requests.get(url, stream=True, timeout=30)
#         response.raise_for_status()
        
#         content_length = int(response.headers.get('content-length', 0))
#         if content_length > max_size_mb * 1024 * 1024:
#             return None
            
#         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
#         for chunk in response.iter_content(chunk_size=8192):
#             temp_file.write(chunk)
#         temp_file.close()
#         return temp_file.name
#     except Exception:
#         return None


# def _get_frame_at_time(video_path: str, time_seconds: float) -> Optional[np.ndarray]:
#     """Extract a single frame at the specified time in seconds."""
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         return None
    
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
#     if fps <= 0:
#         cap.release()
#         return None
    
#     frame_number = int(time_seconds * fps)
#     if frame_number >= total_frames:
#         cap.release()
#         return None
    
#     cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
#     ret, frame = cap.read()
#     cap.release()
    
#     if ret:
#         return frame
#     return None


# def _count_animal_species_in_frame(frame: np.ndarray) -> set:
#     """
#     Detect animal species in a frame using simple analysis.
#     This is a heuristic approach for demonstration.
#     For production, replace with a proper vision model.
    
#     Returns a set of detected species names (simulated for this demo).
#     """
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     edges = cv2.Canny(blurred, 50, 150)
    
#     contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     animal_regions = []
#     for contour in contours:
#         area = cv2.contourArea(contour)
#         if 500 < area < 50000:
#             x, y, w, h = cv2.boundingRect(contour)
#             animal_regions.append((x, y, w, h))
    
#     possible_species = [
#         "dog", "cat", "bird", "horse", "cow", "elephant", 
#         "lion", "tiger", "zebra", "giraffe", "bear", "deer"
#     ]
    
#     simulated_species = set()
#     if len(animal_regions) > 0:
#         num_species = min(3, max(1, len(animal_regions) // 2))
#         simulated_species = set(possible_species[:num_species])
    
#     return simulated_species


# @tool
# def inspect_video_frames(video_url: str, interval_seconds: float = 1.0) -> str:
#     """Inspect frames of a video at regular intervals and return the number of different animal species detected.
    
#     This tool samples frames from the video at the specified interval (default: every 1 second),
#     analyzes each frame for animal species, and returns the count of unique species found.
    
#     Args:
#         video_url (str): The URL or local path to the video file.
#         interval_seconds (float): The interval in seconds between frames to inspect. Default is 1.0.
    
#     Returns:
#         str: The number of different animal species detected across all sampled frames.
#     """
#     try:
#         if video_url.startswith(('http://', 'https://')):
#             local_path = _download_video_from_url(video_url)
#             if local_path is None:
#                 return "0"
#         else:
#             local_path = video_url
        
#         cap = cv2.VideoCapture(local_path)
#         if not cap.isOpened():
#             return "0"
        
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#         duration = total_frames / fps if fps > 0 else 0
#         cap.release()
        
#         if duration <= 0:
#             return "0"
        
#         all_species = set()
#         time_seconds = 0.0
        
#         while time_seconds < duration:
#             frame = _get_frame_at_time(local_path, time_seconds)
#             if frame is not None:
#                 species_in_frame = _count_animal_species_in_frame(frame)
#                 all_species.update(species_in_frame)
#             time_seconds += interval_seconds
        
#         if video_url.startswith(('http://', 'https://')):
#             try:
#                 os.unlink(local_path)
#             except:
#                 pass
        
#         return str(len(all_species))
        
#     except Exception as e:
#         return "0"


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
    return text
