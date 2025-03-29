import json
import os
import sys
import threading
import numpy as np
import pandas as pd
from agent import agent_executor
from json_to_markdown import json_to_markdown  # 引入 markdown 转换函数

# 指定 JSON & Markdown 输出路径
output_json_path = "output.json"
output_md_path = "output.md"

# 运行 Agent
try:
    print("> Running agent...")
    response = agent_executor.invoke({
        "input": " ",
        "tool_names": ", ".join([tool.name for tool in agent_executor.tools]),
        "tool_description": "\n".join(
            [f"- {tool.name}: {tool.description}" for tool in agent_executor.tools]
        ),
    })
    print("> Agent execution finished.")

    # 处理 JSON 序列化的转换函数
    def json_serializable(obj):
        """ 确保所有数据都可被 JSON 序列化 """
        if isinstance(obj, pd.DataFrame):
            return obj.head(5).to_dict(orient="records")  # 只存前5行
        elif isinstance(obj, np.ndarray):
            return obj.tolist()  # numpy 数组转换
        elif isinstance(obj, (np.float32, np.float64)):
            return float(obj)  # numpy 浮点数
        elif isinstance(obj, (np.int32, np.int64)):
            return int(obj)  # numpy 整数
        else:
            return str(obj)  # 兜底方案

    # 处理 intermediate_steps
    if "intermediate_steps" in response:
        response["intermediate_steps"] = [
            {
                "tool": step[0].tool if hasattr(step[0], "tool") else "Unknown",
                "tool_input": step[0].tool_input if hasattr(step[0], "tool_input") else "Unknown",
                "log": step[0].log if hasattr(step[0], "log") else "No log available",
                "result": json_serializable(step[1]) if len(step) > 1 else "No result"
            }
            for step in response["intermediate_steps"]
        ]

    # 保存 JSON
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(response, json_file, indent=4, ensure_ascii=False, default=json_serializable)

    print(f"> Output saved to {output_json_path}")

    # **调用 Markdown 生成**
    json_to_markdown(output_json_path, output_md_path)

    # 终止所有子线程
    if isinstance(response, dict) and "output" in response:
        if "Final Answer" in response["output"]:
            print("> Detected Final Answer, terminating process.")
            for thread in threading.enumerate():
                if thread is not threading.main_thread():
                    thread.join(timeout=1)
                    print(f"> Stopping thread {thread.name}")
            os._exit(0)

    print("> Execution completed, but no Final Answer detected.")
    os._exit(0)

except Exception as e:
    print(f"Error occurred: {repr(e)}", file=sys.stderr)
    os._exit(1)
