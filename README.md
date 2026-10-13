---
title: GAIA Benchmark Agent - HF Agent Course Final
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "4.42.0"
python_version: "3.13.x"
app_file: app.py
pinned: false
---

# Hugging Face Agent Course - Final Unit Assignment

**GAIA Benchmark Agent for Unit 4 Evaluation**

This agent is designed to tackle subset of 20 level 1 questions from the GAIA (General AI Assistant) benchmark as part of the Hugging Face Agent Course final assessment. It uses a LangGraph-based architecture with the Mistral model and specialized tools to handle various question types.

---

## Agent Overview

### Architecture
- **Core Model**: Mistral AI (text-based reasoning)
- **Framework**: LangGraph (stateful multi-tool workflow)
- **Interface**: Gradio (web-based evaluation runner)
- **Tracing**: Langfuse (for debugging and monitoring)

### Workflow
1. Fetches questions from the GAIA benchmark API (`agents-course-unit4-scoring.hf.space`)
2. Processes each question through the LangGraph agent
3. Uses appropriate tools based on question requirements
4. Submits answers and displays results

---

## Capabilities

The agent can successfully handle the following question types from the GAIA benchmark:

### 1. **Web Search & Research**
- **Tool**: `search_tool` (DuckDuckGo Search)

### 2. **Web Page Analysis**
- **Tool**: `fetch_page`
- **Use Case**: Questions requiring detailed information from specific web pages, articles, or papers

### 3. **YouTube Video Transcript Analysis**
- **Tool**: `get_youtube_transcript`
- **Use Case**: Questions about YouTube video speech content
- **Note**: Only works if transcripts are available for the video

---

## Issue

Unless it is a mistake from my side, it prevents to answer the questions with a file associated. A bypass could be to go download each attachment from the GAIA benchmark directly.

The Hugging Face Space endpoint for task files returns `404 Not Found` errors:
```
fetch task file <Response [404]> taskid cca530fc-4052-43b2-b130-b30968d8aa44
url https://agents-course-unit4-scoring.hf.space/files/cca530fc-4052-43b2-b130-b30968d8aa44
```

**Affected Question Types**:
- ✗ **Audio Transcription**: Cannot process audio files
- ✗ **Chess Position Analysis**: Cannot access chess position images
- ✗ **Code Execution**: Cannot execute or analyze attached code files
- ✗ **Spreadsheet Reading**: Cannot read or process spreadsheet data
- ✗ **Document Analysis**: Cannot access attached PDFs, Word docs, etc.

---

## 🔧 Setup Instructions

### Prerequisites
- Python 3.13.x
- Hugging Face account (for submission)
- Mistral API key (set as `LANGCHAIN_MISTRAL_API_KEY`)
- Langfuse credentials (optional, for tracing)

### Installation
```bash
# Clone the repository
git clone https://github.com/boristrs/hf_agent_course_final_project
cd Agent_Course_Final_Assignment

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables
```env
# Required
LANGCHAIN_MISTRAL_API_KEY=your_mistral_api_key

# Optional (for Langfuse tracing)
LANGFUSE_SECRET_KEY=your_langfuse_secret
LANGFUSE_PUBLIC_KEY=your_langfuse_public
LANGFUSE_BASE_URL=https://cloud.langfuse.com

# Hugging Face Space (auto-set when deployed)
SPACE_ID=your_space_id
SPACE_HOST=your_space_host
```

### Running Locally
```bash
python app.py
```
- Opens Gradio interface at `http://localhost:7860`
- Click "Run Evaluation & Submit All Answers"
- Log in with Hugging Face account

---

## 📄 File Structure

```
Agent_Course_Final_Assignment/
├── app.py                  # Main Gradio application
├── gaia_agent.py          # LangGraph agent definition
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── README.md               # This file
├── image_tools.py          # Image processing tools
├── search_tools.py         # Web search tools
├── video_tools.py          # Video processing tools
└── .env                    # Environment variables (not tracked)
```
