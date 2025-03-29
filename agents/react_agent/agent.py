from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAI
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod
from langchain.tools import Tool

from dotenv import load_dotenv
import yaml
from typing import Literal
import uuid
import os

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
deepinfra_api_key = os.getenv("DEEPINFRA_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

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

import json
from langchain.tools import BaseTool
from pydantic import ValidationError

import json
import inspect
from functools import wraps

import json
import inspect
from functools import wraps

def safe_tool_wrapper(tool_func):
    """包装工具，确保 LLM 在调用工具时获取正确的参数格式，并处理 LangChain 传递的额外参数"""
    @wraps(tool_func)
    def wrapper(tool_input, *args, **kwargs):  # ✅ 允许 `callbacks` 和其他额外参数
        try:
            tool_name = getattr(tool_func, "name", "unknown_tool")  # ✅ 这样不会报错
            tool_description = getattr(tool_func, "description", "No description available.")

            # 1️⃣ 获取工具的参数列表和默认值
            sig = inspect.signature(tool_func.func)  # ✅ 需要访问原始 `func` 方法
            expected_params = list(sig.parameters.keys())
            default_values = {k: v.default for k, v in sig.parameters.items() if v.default is not inspect.Parameter.empty}

            # 2️⃣ 解析 `tool_input`
            if isinstance(tool_input, str):
                try:
                    tool_input = json.loads(tool_input)  # 尝试 JSON 解析
                except json.JSONDecodeError:
                    # 3️⃣ 尝试解析逗号分隔字符串
                    parts = [p.strip() for p in tool_input.split(",")]  # ✅ 允许不同间隔的逗号
                    if len(parts) == len(expected_params):  
                        tool_input = dict(zip(expected_params, parts))
                    else:
                        return {
                            "error": f"Invalid input format for {tool_name}. Expected: {expected_params}, but got {len(parts)} values.",
                            "tool_description": tool_description
                        }

            # 4️⃣ 确保 `tool_input` 是字典
            if not isinstance(tool_input, dict):
                return {
                    "error": f"Expected a JSON object for {tool_name}, but received: {type(tool_input).__name__}",
                    "tool_description": tool_description
                }

            # 5️⃣ 检查缺失参数并填充默认值
            missing_params = [p for p in expected_params if p not in tool_input]
            if missing_params:
                for param in missing_params:
                    if param in default_values:
                        tool_input[param] = default_values[param]  # ✅ 使用默认值填充
                    else:
                        return {
                            "error": f"Missing required parameters for {tool_name}: {missing_params}",
                            "tool_description": tool_description
                        }

            # 6️⃣ 调用工具
            return tool_func.func(**tool_input)  # ✅ 访问 `func` 以调用原始 Python 函数

        except Exception as e:
            return {
                "error": f"Error executing tool {tool_name}: {repr(e)}",
                "tool_description": tool_description
            }

    return wrapper

# def safe_tool_wrapper(tool_func):
#     """包装工具，确保 LLM 在调用工具时获取正确的参数格式，并处理 LangChain 传递的额外参数"""
#     @wraps(tool_func)
#     def wrapper(tool_input, *args, **kwargs):
#         try:
#             tool_name = getattr(tool_func, "name", "unknown_tool")
#             tool_description = getattr(tool_func, "description", "No description available.")

#             # 1️⃣ 获取工具参数签名和默认值
#             sig = inspect.signature(tool_func.func)
#             expected_params = list(sig.parameters.keys())
#             default_values = {
#                 k: v.default
#                 for k, v in sig.parameters.items()
#                 if v.default is not inspect.Parameter.empty
#             }

#             # 2️⃣ 尝试解析输入
#             if isinstance(tool_input, str):
#                 try:
#                     tool_input = json.loads(tool_input)
#                 except json.JSONDecodeError:
#                     return {
#                         "error": f"Invalid input format for {tool_name}. Expected a JSON object like {{\"{expected_params[0]}\": \"...\"}}.",
#                         "tool_description": tool_description
#                     }

#             # 3️⃣ 确保是字典
#             if not isinstance(tool_input, dict):
#                 return {
#                     "error": f"Expected a JSON object for {tool_name}, but received: {type(tool_input).__name__}",
#                     "tool_description": tool_description
#                 }

#             # 4️⃣ 补齐默认值或报缺参错
#             missing_params = [p for p in expected_params if p not in tool_input]
#             for param in missing_params:
#                 if param in default_values:
#                     tool_input[param] = default_values[param]
#                 else:
#                     return {
#                         "error": f"Missing required parameters for {tool_name}: {missing_params}",
#                         "tool_description": tool_description
#                     }

#             # 5️⃣ 调用工具本体
#             return tool_func.func(**tool_input)

#         except Exception as e:
#             return {
#                 "error": f"Error executing tool {tool_name}: {repr(e)}",
#                 "tool_description": tool_description
#             }

#     return wrapper




# 确保每个工具都封装为 Tool 实例
tools = [
    Tool(name="get_csv_features", func=safe_tool_wrapper(get_csv_features), description=get_csv_features.__doc__),
    Tool(name="load_csv_file", func=safe_tool_wrapper(load_csv_file), description=load_csv_file.__doc__),
    Tool(name="extract_single_column", func=safe_tool_wrapper(extract_single_column), description=extract_single_column.__doc__),
    Tool(name="extract_two_columns", func=safe_tool_wrapper(extract_two_columns), description=extract_two_columns.__doc__),
    Tool(name="clean_missing_values", func=safe_tool_wrapper(clean_missing_values), description=clean_missing_values.__doc__),
    Tool(name="normalize_or_standardize_data", func=safe_tool_wrapper(normalize_or_standardize_data), description=normalize_or_standardize_data.__doc__),

    Tool(name="group_and_aggregate", func=safe_tool_wrapper(group_and_aggregate), description=group_and_aggregate.__doc__),
    Tool(name="categorical_distribution_shannon_balance", func=safe_tool_wrapper(categorical_distribution_shannon_balance), description=categorical_distribution_shannon_balance.__doc__),
    Tool(name="categorical_distribution_max_min_ratio", func=safe_tool_wrapper(categorical_distribution_max_min_ratio), description=categorical_distribution_max_min_ratio.__doc__),
    Tool(name="categorical_distribution_entropy", func=safe_tool_wrapper(categorical_distribution_entropy), description=categorical_distribution_entropy.__doc__),
    Tool(name="categorical_distribution_gini", func=safe_tool_wrapper(categorical_distribution_gini), description=categorical_distribution_gini.__doc__),
    Tool(name="categorical_distribution_relative_risk", func=safe_tool_wrapper(categorical_distribution_relative_risk), description=categorical_distribution_relative_risk.__doc__),
    Tool(name="numerical_distribution_skewness", func=safe_tool_wrapper(numerical_distribution_skewness), description=numerical_distribution_skewness.__doc__),
    Tool(name="numerical_distribution_kurtosis", func=safe_tool_wrapper(numerical_distribution_kurtosis), description=numerical_distribution_kurtosis.__doc__),
    Tool(name="numerical_distribution_outlier", func=safe_tool_wrapper(numerical_distribution_outlier), description=numerical_distribution_outlier.__doc__),
    Tool(name="numerical_distribution_cohens_d_mad", func=safe_tool_wrapper(numerical_distribution_cohens_d_mad), description=numerical_distribution_cohens_d_mad.__doc__),
    Tool(name="numerical_distribution_quantile_deviation", func=safe_tool_wrapper(numerical_distribution_quantile_deviation), description=numerical_distribution_quantile_deviation.__doc__),
    Tool(name="categorical_categorical_correlation_cramers_v", func=safe_tool_wrapper(categorical_categorical_correlation_cramers_v), description=categorical_categorical_correlation_cramers_v.__doc__),
    Tool(name="categorical_categorical_correlation_elift", func=safe_tool_wrapper(categorical_categorical_correlation_elift), description=categorical_categorical_correlation_elift.__doc__),
    Tool(name="categorical_categorical_correlation_statistical_parity", func=safe_tool_wrapper(categorical_categorical_correlation_statistical_parity), description=categorical_categorical_correlation_statistical_parity.__doc__),
    Tool(name="categorical_categorical_correlation_lipschitz", func=safe_tool_wrapper(categorical_categorical_correlation_lipschitz), description=categorical_categorical_correlation_lipschitz.__doc__),
    Tool(name="categorical_categorical_correlation_total_variation", func=safe_tool_wrapper(categorical_categorical_correlation_total_variation), description=categorical_categorical_correlation_total_variation.__doc__),
    Tool(name="categorical_numerical_correlation_max_abs_mean", func=safe_tool_wrapper(categorical_numerical_correlation_max_abs_mean), description=categorical_numerical_correlation_max_abs_mean.__doc__),
    Tool(name="categorical_numerical_correlation_cohens_d", func=safe_tool_wrapper(categorical_numerical_correlation_cohens_d), description=categorical_numerical_correlation_cohens_d.__doc__),
    Tool(name="categorical_numerical_correlation_standardized_difference", func=safe_tool_wrapper(categorical_numerical_correlation_standardized_difference), description=categorical_numerical_correlation_standardized_difference.__doc__),
    Tool(name="categorical_numerical_correlation_causal_effect", func=safe_tool_wrapper(categorical_numerical_correlation_causal_effect), description=categorical_numerical_correlation_causal_effect.__doc__),
    Tool(name="categorical_numerical_correlation_pse", func=safe_tool_wrapper(categorical_numerical_correlation_pse), description=categorical_numerical_correlation_pse.__doc__),
    Tool(name="numerical_numerical_correlation_pearson", func=safe_tool_wrapper(numerical_numerical_correlation_pearson), description=numerical_numerical_correlation_pearson.__doc__),
    Tool(name="numerical_numerical_correlation_nmi", func=safe_tool_wrapper(numerical_numerical_correlation_nmi), description=numerical_numerical_correlation_nmi.__doc__),
    Tool(name="numerical_numerical_correlation_hgr_approximation", func=safe_tool_wrapper(numerical_numerical_correlation_hgr_approximation), description=numerical_numerical_correlation_hgr_approximation.__doc__),
    Tool(name="numerical_numerical_correlation_wasserstein", func=safe_tool_wrapper(numerical_numerical_correlation_wasserstein), description=numerical_numerical_correlation_wasserstein.__doc__),
    Tool(name="numerical_numerical_correlation_hsic", func=safe_tool_wrapper(numerical_numerical_correlation_hsic), description=numerical_numerical_correlation_hsic.__doc__),

    Tool(name="plot_bar_chart", func=safe_tool_wrapper(plot_bar_chart), description=plot_bar_chart.__doc__),
    Tool(name="plot_pie_chart", func=safe_tool_wrapper(plot_pie_chart), description=plot_pie_chart.__doc__),
    Tool(name="plot_horizontal_bar_chart", func=safe_tool_wrapper(plot_horizontal_bar_chart), description=plot_horizontal_bar_chart.__doc__),
    Tool(name="plot_treemap", func=safe_tool_wrapper(plot_treemap), description=plot_treemap.__doc__),
    Tool(name="plot_heatmap", func=safe_tool_wrapper(plot_heatmap), description=plot_heatmap.__doc__),
    Tool(name="plot_correlation_heatmap", func=safe_tool_wrapper(plot_correlation_heatmap), description=plot_correlation_heatmap.__doc__),
    Tool(name="plot_stacked_bar_chart", func=safe_tool_wrapper(plot_stacked_bar_chart), description=plot_stacked_bar_chart.__doc__),
    Tool(name="plot_grouped_bar_chart", func=safe_tool_wrapper(plot_grouped_bar_chart), description=plot_grouped_bar_chart.__doc__),
    # Tool(name="plot_box_plot", func=safe_tool_wrapper(plot_box_plot), description=plot_box_plot.__doc__),

    Tool(name="get_user_input_tool", func=safe_tool_wrapper(get_user_input_tool), description=get_user_input_tool.__doc__),
    Tool(name="get_all_reference_intentions", func=safe_tool_wrapper(get_all_reference_intentions), description=get_all_reference_intentions.__doc__),
    Tool(name="get_reference_method_by_id", func=safe_tool_wrapper(get_reference_method_by_id), description=get_reference_method_by_id.__doc__),
    Tool(name="generate_bias_report_pdf", func=safe_tool_wrapper(generate_bias_report_pdf), description=generate_bias_report_pdf.__doc__),
    Tool(name="execute_python_code", func=safe_tool_wrapper(execute_python_code), description=execute_python_code.__doc__)
]

tool_names = [tool.name for tool in tools]  # 提取工具的名称列表
tool_names = ", ".join([tool.name for tool in tools])  # 变成逗号分隔的字符串
tool_descriptions = "\n".join(
    [f"- {tool.name}: {tool.description}" for tool in tools]  # 变成字符串
)

from langchain.schema import AgentFinish

from langchain.schema import AgentFinish

def _take_next_step(self, intermediate_steps, **kwargs):
    """如果 `Agent` 生成 `Final Answer`，立刻终止执行"""

    # **让 LLM 生成下一个 Action**
    next_step_output = self._action_agent.plan(intermediate_steps, **kwargs)

    # **如果 `Final Answer` 存在，则立刻终止**
    if isinstance(next_step_output, AgentFinish):
        print("> Finished chain.")  # ✅ 终端输出
        exit(0)  # ✅ 直接终止 Python 进程

    return next_step_output




from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

# 读取 prompts.yaml
with open("prompts.yaml", "r", encoding='utf-8') as file:
    prompt_data = yaml.safe_load(file)
agent_prompt = prompt_data['agent_prompt']


# 创建包含 System Message 的 ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("user", agent_prompt)  # 你的自定义 Agent Prompt
])


from langchain.schema import AgentFinish
import os

# Choose the LLM to use
#########
#invoke GPT 4o
#########
# llm = ChatOpenAI(model="gpt-4o", temperature=0,api_key=openai_api_key)


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

# Construct the ReAct agent
agent = create_react_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True,  return_intermediate_steps=True, max_iterations=50)

import os
import sys

if __name__ == "__main__":
    try:
        response = agent_executor.invoke({
            "input": " ",
            "tool_names": tool_names,
            "tool_description": tool_descriptions,
        })

        print(response)

    except Exception as e:
        print(f"Error occurred: {repr(e)}", file=sys.stderr)
        os._exit(1)


