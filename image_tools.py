import requests
from langchain_core.tools import tool

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