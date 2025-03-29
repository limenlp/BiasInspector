# main.py
import uuid
import json
import os
from datetime import datetime

from agent import graph
from json_to_markdown import json_to_markdown

# Configure initial parameters
thread_id = str(uuid.uuid4())
config = {
    "configurable": {
        "passenger_id": "3442 587242",
        "thread_id": thread_id
    },
    "recursion_limit": 100
}

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
            current_state = 'Execution Assistant'
        elif message_type == 'tool':
            current_state = 'Execution_Tools'
        elif message_type == 'system':
            current_state = 'SystemMessageNode'
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

# Initialize questions
initial_questions = [
    "Hi there, what can you do for me?",
 
    # "Detect whether there is correlation relation between race and insurance in dataset:source_files/example_raw_data.csv",
    # "Detect whether there is distribution bias for gender in dataset:source_files/example_raw_data.csv",
    # "Detect whether there is correlation relation between race and insurance in dataset:source_files/example_raw_data_withBias.csv",
    # "Detect whether there is correlation relation between race and insurance in dataset:source_files/example_raw_data.csv, read reference papers before you generate decision",
]

# Process event stream and output results
_printed = set()
log_data = []

for question in initial_questions:
    print("\n================================== Human Message =================================\n")
    print(question)
    events = graph.stream(
        {"messages": ("user", question)},
        config,
        stream_mode="values",
    )
    for event in events:
        event_handler(event, _printed, log_data)

# Generate a unique filename with timestamp
timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"agent_log_{timestamp_str}.json"
log_filepath = os.path.join('logs', log_filename)

# Write log data to JSON file
with open(log_filepath, 'w', encoding='utf-8') as f:
    json.dump(log_data, f, ensure_ascii=False, indent=4)

# After generating logs, execute json_to_markdown.py
json_to_markdown(json_file_path=log_filepath) 
