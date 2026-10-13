from io import BytesIO
import os
from typing import Optional
from urllib.parse import urlparse
from wsgiref import headers
import tempfile
import uuid
import requests
from langchain_core.tools import tool
from PIL import Image



@tool
def download_file_from_url(url: str, filename: Optional[str] = None) -> str:
    """
    Download a file from a URL and save it to a temporary location.
    Args:
        url (str): the URL of the file to download.
        filename (str, optional): the name of the file. If not provided, a random name file will be created.
    """
    try:
        # Parse URL to get filename if not provided
        if not filename:
            path = urlparse(url).path
            filename = os.path.basename(path)
            if not filename:
                filename = f"downloaded_{uuid.uuid4().hex[:8]}"

        # Create temporary file
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, filename)

        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Save the file
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return f"File downloaded to {filepath}. You can read this file to process its contents."
    except Exception as e:
        return f"Error downloading file: {str(e)}"



@tool
def fetch_task_file(task_id: str) -> str:
    """
    MUST USE when a question mentions an attached file.
    Input:
    - task_id (string): id of the question.
    Returns:
    - local file path of downloaded file
    After using this tool:
    - You should analyze or execute the file depending on type
    """
    try:
        url = f"https://agents-course-unit4-scoring.hf.space/files/{task_id}"
        response = requests.get(url)
        
        print("fetch task file ",response, "taskid ",task_id, "url ", url)
        
        if response.status_code != 200:
            return f"ERROR: {response.text}"
        
        # Try to detect filename (fallback)
        filename = f"{task_id}"
        
        # Save file
        filepath = f"./downloadsHuggingFace/{filename}"
        os.makedirs("./downloadsHuggingFace", exist_ok=True)
        
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        return filepath

    except Exception as e:
        log_tool("fetch_task_file", task_id, f"ERROR: {str(e)}")
        return f"ERROR: {str(e)}"