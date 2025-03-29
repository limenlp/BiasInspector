import uuid
import json
import os
import random
import time
from datetime import datetime

from agent import create_new_agent
from json_to_markdown import json_to_markdown

# Ensure the 'logs' directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Event stream handling function with JSON logging
def event_handler(event: dict, _printed: set, log_data: list, max_length=5000):
    message = event.get("messages")
    current_state = None  # Initialize current state

    if message:
        if isinstance(message, list):
            message = message[-1]
        # Get message type and name
        message_type = message.type
        assistant_name = getattr(message, 'name', None)

        # Infer current state based on message_type and assistant_name
        if message_type == 'ai':
            current_state = 'Assistant'
        elif message_type == 'tool':
            current_state = 'Tools'
        elif message_type == 'human':
            current_state = 'User Input'
        else:
            current_state = 'Unknown State'

        # Adjust message_type display format
        if message_type == 'ai':
            message_type = 'AI'
        elif message_type == 'human':
            message_type = 'Human'
        elif message_type == 'tool':
            message_type = 'Tool'
        else:
            message_type = message_type.capitalize()

        # Build log entry without assistant_name
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "state": current_state,
            "message_id": message.id,
            "message_type": message_type,
            "message_content": message.content,
            "message_tool_calls": getattr(message, 'tool_calls', None),
        }

        # Add to printed set and print message if not already printed
        if message.id not in _printed:
            if message_type != 'Human':  # Skip printing Human messages
                msg_repr = message.pretty_repr(html=True)
                if len(msg_repr) > max_length:
                    msg_repr = msg_repr[:max_length] + " ... (truncated)"
                print(msg_repr)
            _printed.add(message.id)

    else:
        # If there's no message, still build the log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "state": None,
            "message_id": None,
            "message_type": None,
            "message_content": None,
            "message_tool_calls": None,
        }

    log_data.append(log_entry)

def run_agent_with_logname(log_basename: str):
    # Create a fresh agent per run
    graph = create_new_agent()

    uid = uuid.uuid4().hex[:6]
    distractors = [
        "Approach this file independently of all others.",
        "Reset your thoughts before reviewing.",
        "Do not rely on prior memory or runs.",
        "Treat this markdown as if it's the only one.",
        "Evaluate from scratch without assumptions."
    ]
    interrupt = random.choice(distractors)

    initial_questions = [
        f"{interrupt} (Session: {uid})\n"
        f"Please help me evaluate the bias detection log, markdown log located at source_files/markdown_logs/Llama3.3 70B/ReAct/{log_basename}.md.\n"
        "Examples of the five different levels(higher is better) are stored in the following locations respectively: examples/example_level5.md, examples/example_level4.md, examples/example_level3.md, examples/example_level2.md, examples/example_level1.md.\n"
        "DO NOT generalize across runs. Focus on the unique qualities of this document."
    ]

    _printed = set()
    log_data = []

    for question in initial_questions:
        print("\n================================== Human Message =================================\n")
        print(question)
        thread_id = str(uuid.uuid4())
        config = {
            "configurable": {
                "passenger_id": "3442 587242",
                "thread_id": thread_id
            },
            "recursion_limit": 100
        }
        events = graph.stream(
            {"messages": ("user", question)},
            config,
            stream_mode="values",
        )
        for event in events:
            event_handler(event, _printed, log_data)

    log_filename = f"{log_basename}.json"
    log_filepath = os.path.join('logs', log_filename)

    with open(log_filepath, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=4)

    json_to_markdown(json_file_path=log_filepath)

# 仅在手动运行 main.py 时执行（被 batch_run 调用时不会执行）
if __name__ == "__main__":
    run_agent_with_logname("Correlation_COMPAS_3")