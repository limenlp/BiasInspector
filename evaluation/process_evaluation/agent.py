import yaml
from dotenv import load_dotenv
from typing import Literal

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod

from langchain_openai import ChatOpenAI

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START

from agent_node_factory import *

from tools import (
    get_user_input_tool,
    read_json_log,
    read_markdown_log,
    generate_evaluation_report_pdf
)

# Load environment variables from .env file
load_dotenv()

# Read prompts.yaml file and extract agent prompts
with open('prompts.yaml', 'r', encoding='utf-8') as file:
    prompt_data = yaml.safe_load(file)
prompt = prompt_data['agent']['system_message']

# Create ChatPromptTemplate instance
assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", prompt),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Initialize LLM model
llm = ChatOpenAI(model="o3-mini", temperature=1)

# Define tool list
tools = [
    get_user_input_tool,
    read_json_log,
    read_markdown_log,
    generate_evaluation_report_pdf
]

# Helper function to create a node for a given agent
def agent_node(state, agent, name):
    result = agent.invoke(state)
    if isinstance(result, ToolMessage):
        return {"messages": [result]}
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {"messages": [result]}

# Router function to guide the workflow based on conditions
def router(state) -> Literal["DECISION ANALYSIS", "__end__", "call_tool"]:
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "call_tool"
    if "DECISION ANALYSIS" in last_message.content:
        return "DECISION ANALYSIS"
    if "COMPLETE TASK" in last_message.content:
        return "__end__"
    
    return "DECISION ANALYSIS"

# Create execution tool node with fallback mechanism
def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls 

    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }

def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )

# ===== ✅ 核心改动：封装为函数，每次调用都重新创建干净的 Agent 图 =====
def create_new_agent():
    memory = MemorySaver()  # 每次新建 memory，避免复用状态
    workflow = StateGraph(State)

    assistant_runnable = assistant_prompt | llm.bind_tools(tools)

    workflow.add_node("Assistant", Assistant(assistant_runnable))
    workflow.add_node("Tools", create_tool_node_with_fallback(tools))
    workflow.add_edge("Tools", "Assistant")

    workflow.add_conditional_edges(
        "Assistant",
        router,
        {
            "DECISION ANALYSIS": "Assistant",
            "call_tool": "Tools",  
            "__end__": END,
        },
    )

    workflow.add_edge(START, "Assistant")

    graph = workflow.compile(checkpointer=memory)
    return graph

# ===== ✅ 可选：生成一次性图结构可视化（用于主程序展示结构用） =====
def draw_graph():
    graph = create_new_agent()
    graph.get_graph().draw_mermaid_png(
        curve_style=CurveStyle.LINEAR,
        wrap_label_n_words=9,
        output_file_path='generated_files/agent_graph.png',
        draw_method=MermaidDrawMethod.API,
        background_color="white",
        padding=10,
    )
