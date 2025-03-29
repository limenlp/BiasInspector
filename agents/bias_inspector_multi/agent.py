import uuid
import yaml
from dotenv import load_dotenv
from typing import Literal
import os

from langchain_core.messages import AIMessage, ToolMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START

from agent_node_factory import *
from tools import (
    # Data Loading and Preprocessing Tools
    get_csv_features,
    load_csv_file,
    extract_single_column,
    extract_two_columns,
    clean_missing_values,
    normalize_or_standardize_data,

    # Analysis Tools
    group_and_aggregate,
    categorical_distribution_shannon_balance,
    categorical_distribution_max_min_ratio,
    categorical_distribution_entropy,
    categorical_distribution_gini,
    categorical_distribution_relative_risk,
    numerical_distribution_skewness,
    numerical_distribution_kurtosis,
    numerical_distribution_outlier,
    numerical_distribution_cohens_d_mad,
    numerical_distribution_quantile_deviation,
    categorical_categorical_correlation_cramers_v,
    categorical_categorical_correlation_elift,
    categorical_categorical_correlation_statistical_parity,
    categorical_categorical_correlation_lipschitz,
    categorical_categorical_correlation_total_variation,
    categorical_numerical_correlation_max_abs_mean,
    categorical_numerical_correlation_cohens_d,
    categorical_numerical_correlation_standardized_difference,
    categorical_numerical_correlation_causal_effect,
    categorical_numerical_correlation_pse,
    numerical_numerical_correlation_pearson,
    numerical_numerical_correlation_nmi,
    numerical_numerical_correlation_hgr_approximation,
    numerical_numerical_correlation_wasserstein,
    numerical_numerical_correlation_hsic,

    # Results Presentation Tools
    plot_bar_chart,
    plot_pie_chart,
    plot_horizontal_bar_chart,
    plot_treemap,
    plot_heatmap,
    plot_correlation_heatmap,
    plot_stacked_bar_chart,
    plot_grouped_bar_chart,
    plot_box_plot,

    # Miscellaneous Tools
    get_user_input_tool,
    get_all_reference_intentions,
    get_reference_method_by_id,
    generate_bias_report_pdf,
    execute_python_code
)


# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
deepinfra_api_key = os.getenv("DEEPINFRA_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Read prompts.yaml file and extract agent prompts
with open("prompts.yaml", "r", encoding='utf-8') as file:
    prompt_data = yaml.safe_load(file)
primary_agent_prompt = prompt_data['primary_agent']['system_message']
advisor_agent_prompt = prompt_data['advisor_agent']['system_message']

# Create ChatPromptTemplate instances
primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", primary_agent_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

advisor_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", advisor_agent_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

#########
#invoke GPT 4o
#########
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0,api_key=openai_api_key)


#########
#invoke Llama 3.3 70B
#########
llm = ChatOpenAI(
    model="meta-llama/Llama-3.3-70B-Instruct",  
    base_url="https://api.deepinfra.com/v1/openai",  
    api_key=deepinfra_api_key, 
    temperature=0 
)

#########
#invoke deepseek v3
#########
# llm = ChatOpenAI(
#     model="deepseek-chat",  
#     base_url="https://api.deepseek.com",  
#     api_key=deepseek_api_key, 
#     temperature=0 
# )

#########
#invoke claude
#########
# llm = ChatAnthropic(
#     model_name="claude-3-7-sonnet-20250219",  
#     anthropic_api_key=anthropic_api_key, 
#     temperature=0
# )



# Define tool list
execution_tools = [
    # Data Loading and Preprocessing Tools
    get_csv_features,
    load_csv_file,
    extract_single_column,
    extract_two_columns,
    clean_missing_values,
    normalize_or_standardize_data,

    # Analysis Tools
    group_and_aggregate,
    categorical_distribution_shannon_balance,
    categorical_distribution_max_min_ratio,
    categorical_distribution_entropy,
    categorical_distribution_gini,
    categorical_distribution_relative_risk,
    numerical_distribution_skewness,
    numerical_distribution_kurtosis,
    numerical_distribution_outlier,
    numerical_distribution_cohens_d_mad,
    numerical_distribution_quantile_deviation,
    categorical_categorical_correlation_cramers_v,
    categorical_categorical_correlation_elift,
    categorical_categorical_correlation_statistical_parity,
    categorical_categorical_correlation_lipschitz,
    categorical_categorical_correlation_total_variation,
    categorical_numerical_correlation_max_abs_mean,
    categorical_numerical_correlation_cohens_d,
    categorical_numerical_correlation_standardized_difference,
    categorical_numerical_correlation_causal_effect,
    categorical_numerical_correlation_pse,
    numerical_numerical_correlation_pearson,
    numerical_numerical_correlation_nmi,
    numerical_numerical_correlation_hgr_approximation,
    numerical_numerical_correlation_wasserstein,
    numerical_numerical_correlation_hsic,

    # Results Presentation Tools
    plot_bar_chart,
    plot_pie_chart,
    plot_horizontal_bar_chart,
    plot_treemap,
    plot_heatmap,
    plot_correlation_heatmap,
    plot_stacked_bar_chart,
    plot_grouped_bar_chart,
    plot_box_plot,

    # Miscellaneous Tools
    get_user_input_tool,
    get_all_reference_intentions,
    get_reference_method_by_id,
    generate_bias_report_pdf,
    execute_python_code
]

# Helper function to create a node for a given agent
# Helper function to create a node for a given agent
# def agent_node(state, agent, name):
#     result = agent.invoke(state)
#     if isinstance(result, ToolMessage):
#         return {"messages": [result]}
#     else:
#         result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
#     return {"messages": [result]}



def agent_node(state, agent, name):
    result = agent.invoke(state)

    # print(f"=== Agent [{name}] Debug Info ===")
    # print("Result:", result)

    # **如果有工具调用，先返回工具调用**
    if hasattr(result, "tool_calls") and result.tool_calls:
        print(f"{name} detected tool calls:", result.tool_calls)
        return {"messages": [result]}

    # **避免 `Advisor Assistant` 进入空循环**
    if name == "Advisor_Assistant" and (result is None or not result.content.strip()):
        print(f"Warning: {name} returned empty content. Encouraging new analysis.")
        
        # 获取 `Primary Assistant` 的最新消息
        previous_messages = [msg.content for msg in reversed(state["messages"]) if msg.name == "Primary_Assistant"]
        last_valid_message = previous_messages[0] if previous_messages else "Let's analyze the next step."

        return {"messages": [AIMessage(content=f"{last_valid_message}\n\nLet's refine our approach and ensure we are using the most effective bias detection tools.", name=name)]}

    # **避免 `Primary Assistant` 死循环工具调用**
    if name == "Primary_Assistant" and (result is None or not result.content.strip()):
        print(f"Warning: {name} returned empty content. Fetching previous Advisor Assistant message.")

        # **如果 `Primary Assistant` 触发了工具调用，直接执行工具调用，不要回溯**
        if hasattr(state["messages"][-1], "tool_calls") and state["messages"][-1].tool_calls:
            return {"messages": [state["messages"][-1]]}

        # **否则，获取 `Advisor Assistant` 的最近消息**
        previous_messages = [msg.content for msg in reversed(state["messages"]) if msg.name == "Advisor_Assistant"]
        last_valid_message = previous_messages[0] if previous_messages else "Let's review the results together."

        return {"messages": [AIMessage(content=f"{last_valid_message}", name=name)]}

    return {"messages": [AIMessage(**result.dict(exclude={"type", "name"}), name=name)]}






# Router function to guide the workflow based on conditions
def execution_router(state) -> Literal["DECISION ANALYSIS", "__end__", "call_tool"]:
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

def create_tool_node_with_fallback(tools: list):
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )

# Helper function to create a node for SystemMessage
def system_message_node(state):
    system_message = SystemMessage(content="Remember to call the tool to look up the exact names of each column in the dataset. \n You should call tools to detect, analyze, and generate visual charts.")
    return {"messages": [system_message]}

# Define the workflow
workflow = StateGraph(State)


primary_assistant_runnable = primary_assistant_prompt | llm.bind_tools(execution_tools)
advisor_assistant_runnable = advisor_assistant_prompt | llm.bind_tools(execution_tools)


# Add nodes to the workflow
workflow.add_node("Primary Assistant", lambda state: agent_node(state, primary_assistant_runnable, "Primary_Assistant"))
workflow.add_node("Advisor Assistant", lambda state: agent_node(state, advisor_assistant_runnable, "Advisor_Assistant"))
workflow.add_node("Execution_Tools", create_tool_node_with_fallback(execution_tools))

# Add conditional edges for routing
workflow.add_conditional_edges(
    "Primary Assistant",
    execution_router,
    {
        "DECISION ANALYSIS": "Advisor Assistant",
        "call_tool": "Execution_Tools",
        "__end__": END,
    },
)

workflow.add_conditional_edges(
    "Advisor Assistant",
    execution_router,
    {
        "DECISION ANALYSIS": "Primary Assistant",
        "call_tool": "Execution_Tools",
        "__end__": END,
    },
)

# Add new SystemMessage node to the workflow
workflow.add_node("SystemMessageNode", system_message_node)

# Modify the edge between ToolNode and Primary Assistant
workflow.add_edge("Execution_Tools", "SystemMessageNode")
workflow.add_edge("SystemMessageNode", "Primary Assistant")

workflow.add_edge(START, "Primary Assistant")

# Set up memory saver
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# Generate and save Mermaid image as a PNG file
graph.get_graph().draw_mermaid_png(
    curve_style=CurveStyle.LINEAR,
    wrap_label_n_words=9,
    output_file_path='generated_files/agent_graph.png',
    draw_method=MermaidDrawMethod.API,
    background_color="white",
    padding=10,
)
