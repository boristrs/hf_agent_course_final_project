from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

from search_tools import search_tool
from video_tools import inspect_video_frames, get_youtube_transcript
from image_tools import download_file_from_url, fetch_task_file

import os
from dotenv import load_dotenv

# Generate the chat interface, including the tools
from langchain_mistralai.chat_models import ChatMistralAI

load_dotenv()
LANGCHAIN_MISTRAL_API_KEY = os.getenv("LANGCHAIN_MISTRAL_API_KEY")
model = ChatMistralAI(
    mistral_api_key=LANGCHAIN_MISTRAL_API_KEY,
    temperature=0,
)

SYSTEM_PROMPT = ("""
    You are a general AI assistant.
    I will ask you a question.
    Report your thoughts, and finish your answer with the following template: YOUR FINAL ANSWER: <your answer here>
    Your final answer must be a number OR as few words as possible OR a comma separated list of numbers and/or strings.
    If you are asked for a number, don't use comma to write your number neither use units such as $ or percent sign unless specified otherwise.
    If you are asked for a string, don't use articles, neither abbreviations (e.g. for cities), and write the digits in plain text unless specified otherwise.
    If you are asked for a comma separated list, apply the above rules depending of whether the element to be put in the list is a number or a string.
""")

tools = [search_tool, inspect_video_frames, get_youtube_transcript, download_file_from_url, fetch_task_file]
chat_with_tools = model.bind_tools(tools)

# Generate the AgentState and Agent graph
class AgentState(TypedDict):
    question: str
    file_name: str
    task_id: str
    messages: Annotated[list[AnyMessage], add_messages]

def assistant(state: AgentState):
    user_content = state["question"]
    if state.get("task_id"):
        user_content += f"\n\nTASK_ID: {state['task_id']}"
    if state.get("file_name"):
        user_content += f"\nFILE_NAME: {state['file_name']}"
    response = chat_with_tools.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_content),
        *state["messages"],
    ])
    return {"messages": [response]}

## The graph
builder = StateGraph(AgentState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message requires a tool, route to tools
    # Otherwise, provide a direct response
    tools_condition,
)
builder.add_edge("tools", "assistant")

