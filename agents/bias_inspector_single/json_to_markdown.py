import json
import os
from datetime import datetime

def json_to_markdown(json_file_path, output_dir='markdown_logs'):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate a unique filename for the markdown file
    base_name = os.path.basename(json_file_path)
    name_without_ext = os.path.splitext(base_name)[0]
    markdown_filename = f"{name_without_ext}.md"
    markdown_filepath = os.path.join(output_dir, markdown_filename)
    
    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        log_data = json.load(f)
    
    # Start writing to the markdown file
    with open(markdown_filepath, 'w', encoding='utf-8') as md_file:
        md_file.write(f"# Log File: {base_name}\n\n")
        md_file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        md_file.write("---\n\n")
        
        for entry in log_data:
            state = entry.get('state', 'N/A')
            # Skip entries where state is 'SystemMessageNode'
            if state == 'SystemMessageNode':
                continue  # Skip this entry

            timestamp = entry.get('timestamp', 'N/A')
            message_type = entry.get('message_type', 'N/A')
            message_id = entry.get('message_id', 'N/A')
            message_content = entry.get('message_content', '')
            message_tool_calls = entry.get('message_tool_calls', None)
            
            md_file.write(f"## {state}\n")
            md_file.write(f"- **Timestamp**: {timestamp}\n")
            md_file.write(f"- **Message Type**: {message_type}\n")
            md_file.write(f"- **Message ID**: {message_id}\n\n")
            md_file.write(f"### Message Content:\n\n{message_content}\n\n")
            
            if message_tool_calls:
                md_file.write(f"### Tool Calls:\n")
                for tool_call in message_tool_calls:
                    tool_name = tool_call.get('name', 'N/A')
                    tool_args = tool_call.get('args', {})
                    tool_id = tool_call.get('id', 'N/A')
                    md_file.write(f"- **Tool Name**: {tool_name}\n")
                    md_file.write(f"  - **Tool ID**: {tool_id}\n")
                    md_file.write(f"  - **Arguments**: {json.dumps(tool_args, ensure_ascii=False)}\n")
            md_file.write("\n---\n\n")
    
    print(f"Markdown file generated at: {markdown_filepath}")

if __name__ == "__main__":
    # Example usage
    # Replace 'log/agent_log_YYYYMMDD_HHMMSS.json' with your actual JSON log file path
    json_log_file = 'logs/agent_log_20240914_224326.json'
    json_to_markdown(json_log_file)
