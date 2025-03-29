import json

def json_to_markdown(json_path="output.json", md_path="output.md"):
    """ 读取 JSON 并转换为 Markdown 格式 """
    
    # 读取 JSON 文件
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # 生成 Markdown 文本
    md_content = []

    # 标题
    md_content.append(f"# Bias Detection Report\n")

    # **输入部分**
    md_content.append(f"## Input")
    md_content.append(f"**User Request:** {data.get('input', 'N/A')}\n")

    # **工具描述**
    md_content.append(f"## Tools Used")
    md_content.append(f"**Available Tools:**\n")
    tools = data.get("tool_names", "").split(", ")
    for tool in tools:
        md_content.append(f"- `{tool}`")

    # **分析结果**
    md_content.append(f"## Final Analysis")
    md_content.append(f"**Conclusion:**\n\n{data.get('output', 'N/A')}\n")

    # **详细执行步骤**
    md_content.append(f"## Execution Steps")
    intermediate_steps = data.get("intermediate_steps", [])

    for step in intermediate_steps:
        md_content.append(f"### Tool: `{step['tool']}`")
        md_content.append(f"- **Input:** `{step['tool_input']}`")
        md_content.append(f"- **Log:** {step['log']}")
        
        result = step.get("result", "No result")
        if isinstance(result, list):
            md_content.append("- **Result:**\n")
            for item in result[:5]:  # 仅显示前5个数据，避免过长
                md_content.append(f"  - {item}")
        else:
            md_content.append(f"- **Result:** `{result}`")

        md_content.append("\n---\n")  # 分隔线

    # **保存 Markdown 文件**
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write("\n".join(md_content))

    print(f"> Markdown report saved as {md_path}")

# 允许被 main.py 调用
if __name__ == "__main__":
    json_to_markdown()
