import os
import re
import json
from typing import Annotated
from fpdf import FPDF
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from PyPDF2 import PdfReader


# ======================================
# - get_user_input_tool: Captures user input dynamically during an interaction and formats it as a dictionary to be added to the Agent's conversation.  
#   Input: None. Output: User input message (dict) or error message (str).
#
# - read_json_log: Reads a JSON formatted log file, extracting and organizing log entries.
#   Input: log_file_path (str). Output: A dictionary (dict) containing the extracted log entries, or an error message (str) if the process fails.
#   
# - read_markdown_log: Reads a Markdown formatted log file, extracting headers, bold text, and regular text as log entries.
#   Input: log_file_path (str). Output: A dictionary (dict) containing extracted log entries, including headers (with levels), bold text, and regular text, or an error message (str) if the process fails.
#   
# - read_bias_report_pdf: Reads a bias detection report in PDF format, extracting both text and image information.
#   Input: input_pdf_path (str). Output: A dictionary (dict) containing the extracted sections of the report, which can include text and image entries, or an error message (str) if the process fails.
#   
# - generate_evaluation_report_pdf: Generates a flexible evaluation report in PDF format, combining text and charts as specified in the input.
#   Input: content_sections (list[dict]), output_pdf_path (str). Output: Success message (str) or error message (str).
#
# ======================================
@tool
def get_user_input_tool() -> dict:
    """
    Get user input dynamically during an ongoing interaction with the Agent.

    Returns:
        dict: A dictionary representing the user's input message to be added to the Agent's conversation.
    """
    try:
        user_input_content = input("(Send a message to the Agent): ")

        combined_message = f"{user_input_content}."

        user_message = {
            "messages": [
                HumanMessage(
                    content=combined_message
                )
            ],
            "sender": "Human"
        }

        return user_message
    
    except Exception as e:
        return {
            "error": f"Failed to get user input. Error: {repr(e)}"
        }

@tool
def read_json_log(
    log_file_path: Annotated[str, "The path of the JSON log file to read."]
) -> dict:
    """
    Read a JSON formatted log file, extracting and organizing log entries.

    Args:
        log_file_path (str): The path of the JSON log file to read.

    Returns:
        dict: A dictionary containing extracted log entries.
              Example:
              {
                  "logs": [
                      {"timestamp": "2023-09-26T12:00:00", "level": "INFO", "message": "Process started."},
                      {"timestamp": "2023-09-26T12:01:00", "level": "ERROR", "message": "Failed to connect to database."}
                  ]
              }
    """
    try:
        # Open and read the JSON log file
        with open(log_file_path, 'r') as log_file:
            log_data = json.load(log_file)
        
        extracted_logs = {"logs": []}

        # Process each log entry
        for log_entry in log_data:
            timestamp = log_entry.get("timestamp", "N/A")
            level = log_entry.get("level", "N/A")
            message = log_entry.get("message", "No message provided")

            extracted_logs["logs"].append({
                "timestamp": timestamp,
                "level": level,
                "message": message
            })

        return extracted_logs

    except FileNotFoundError:
        return f"Log file not found: {log_file_path}"

    except json.JSONDecodeError:
        return f"Failed to decode JSON log file: {log_file_path}"

    except Exception as e:
        return f"Failed to read JSON log file. Error: {repr(e)}"

import re

@tool
def read_markdown_log(
    log_file_path: Annotated[str, "The path of the Markdown log file to read."]
) -> dict:
    """
    Read a Markdown formatted log file, extracting headers, bold text, and regular text as log entries.

    Args:
        log_file_path (str): The path of the Markdown log file to read.

    Returns:
        dict: A dictionary containing extracted log entries.
              Example:
              {
                  "logs": [
                      {"type": "header", "level": 1, "content": "Log Start"},
                      {"type": "text", "content": "This is a log entry."},
                      {"type": "bold", "content": "Important information."}
                  ]
              }
    """
    try:
        with open(log_file_path, 'r', encoding='utf-8') as log_file:
            lines = log_file.readlines()
        
        extracted_logs = {"logs": []}

        # Process each line to detect markdown elements
        for line in lines:
            line = line.strip()
            
            # Detect headers (e.g., # Header1, ## Header2, ### Header3)
            header_match = re.match(r'^(#+)\s+(.*)', line)
            if header_match:
                header_level = len(header_match.group(1))  # Count number of '#' to determine header level
                header_content = header_match.group(2)
                extracted_logs["logs"].append({
                    "type": "header",
                    "level": header_level,
                    "content": header_content
                })
            
            # Detect bold text (e.g., **bold text**)
            elif re.match(r'\*\*(.*?)\*\*', line):
                bold_content = re.sub(r'\*\*(.*?)\*\*', r'\1', line)  # Remove ** to extract bold text
                extracted_logs["logs"].append({
                    "type": "bold",
                    "content": bold_content
                })

            # Regular text (any line that is not a header or bold)
            elif line:
                extracted_logs["logs"].append({
                    "type": "text",
                    "content": line
                })

        return extracted_logs

    except FileNotFoundError:
        return f"Markdown log file not found: {log_file_path}"

    except Exception as e:
        return f"Failed to read Markdown log file. Error: {repr(e)}"


# @tool
# def read_bias_report_pdf(input_pdf_path):
#     """
#     Read a bias detection report in PDF format, extracting text content.

#     Args:
#         input_pdf_path (str): The path of the PDF report to read.

#     Returns:
#         dict: A dictionary containing extracted text information. 
#               Example:
#               {
#                   "sections": [
#                       {"type": "text", "content": "This is the report introduction."},
#                       {"type": "text", "content": "Here is the analysis for section 2."}
#                   ]
#               }
#     """
#     # Get absolute path of the PDF
#     input_pdf_path = os.path.abspath(input_pdf_path)
#     print(f"Absolute PDF Path: {input_pdf_path}")

#     # Check if the file exists
#     if not os.path.exists(input_pdf_path):
#         return {"error": f"File does not exist: {input_pdf_path}"}

#     try:
#         # Initialize PDF reader and open the PDF file
#         reader = PdfReader(input_pdf_path)
#         total_pages = len(reader.pages)
#         extracted_content = {"sections": []}

#         # Iterate through each page and extract text
#         for page_num in range(total_pages):
#             page = reader.pages[page_num]
#             page_text = page.extract_text()

#             if page_text:
#                 # Split text by lines and add each line to the content
#                 lines = page_text.split('\n')
#                 for line in lines:
#                     extracted_content["sections"].append({"type": "text", "content": line})

#         return extracted_content

#     except Exception as e:
#         return {"error": f"Failed to read PDF report. Error: {repr(e)}"}


@tool
def generate_evaluation_report_pdf(
    content_sections: Annotated[list[dict], "List of content sections, where each section can be either text or an image."],
    output_pdf_path: Annotated[str, "The path to save the generated PDF report."]
) -> str:
    """
    Generate a flexible evaluation report in PDF format, including both text and charts.

    Args:
        content_sections (list[dict]): A list of content sections where each section is a dict with keys
                                       'type' (either 'text' or 'image') and corresponding content.
                                       Example:
                                       [
                                           {"type": "text", "content": "This is a report introduction."},
                                           {"type": "image", "content": "path_to_image1.png"},
                                           {"type": "text", "content": "Here is the analysis for section 2."},
                                           {"type": "image", "content": "path_to_image2.png"}
                                       ]
        output_pdf_path (str): The path to save the generated PDF report.

    Returns:
        str: A message indicating whether the PDF report was successfully created and saved,
             or an error message if the process failed.
    """
    try:
        # Create FPDF object
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Add a title page
        pdf.add_page()
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(0, 10, 'Evaluation Report', ln=True, align='C')
        pdf.ln(12)

        # Process the content sections
        for section in content_sections:
            if section['type'] == 'text':
                # Add logic for handling Markdown-like syntax (e.g., '###' for headers)
                text_content = section['content']
                lines = text_content.split('\n')  # Split into lines

                for line in lines:
                    # Regex pattern to detect ![Chart Title](path/to/chart.png)
                    match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
                    if match:
                        # Extract chart title and image path
                        chart_title = match.group(1)
                        image_path = match.group(2)

                        if os.path.exists(image_path):
                            pdf.set_font('Arial', 'B', 12)
                            pdf.cell(0, 10, chart_title, ln=True, align='C')  # Display chart title
                            pdf.image(image_path, x=(210 - 100) / 2, w=100)  # Insert and center image
                            pdf.ln(10)  # Add space after the image
                        else:
                            pdf.cell(0, 10, f'Image not found: {image_path}', ln=True)
                            pdf.ln(10)

                    elif line.startswith('### '):
                        # Process as a level 3 header
                        header_text = line.replace('### ', '')  # Remove '### '
                        pdf.set_font('Arial', 'B', 14)  # Set font to bold and slightly larger
                        pdf.cell(0, 10, header_text, ln=True)
                        pdf.ln(5)  # Add space after header

                    elif line.startswith('## '):
                        # Process as a level 2 header
                        header_text = line.replace('## ', '')  # Remove '## '
                        pdf.set_font('Arial', 'B', 16)  # Set font to bold and larger
                        pdf.cell(0, 10, header_text, ln=True)
                        pdf.ln(5)  # Add space after header

                    elif line.startswith('# '):
                        # Process as a level 1 header
                        header_text = line.replace('# ', '')  # Remove '# '
                        pdf.set_font('Arial', 'B', 18)  # Set font to bold and larger
                        pdf.cell(0, 10, header_text, ln=True)
                        pdf.ln(5)  # Add space after header

                    elif line.startswith('#### '):
                        # Process as a level 4 header
                        header_text = line.replace('#### ', '')  # Remove '#### '
                        pdf.set_font('Arial', 'B', 13)  # Set font to bold and larger
                        pdf.cell(0, 10, header_text, ln=True)
                        pdf.ln(5)  # Add space after header

                    elif line.startswith('**'):
                        # Process as bold text
                        bold_text = line.replace('**', '')
                        pdf.set_font('Arial', 'B', 12)
                        pdf.multi_cell(190, 10, bold_text)
                        pdf.ln(5)  # Add space after bold text

                    else:
                        # Process as regular text
                        pdf.set_font('Arial', '', 12)
                        pdf.multi_cell(190, 10, line)
                        pdf.ln(5)

            elif section['type'] == 'image':
                # Add image content
                image_path = section['content']
                if os.path.exists(image_path):
                    # Reduce image size and center it
                    pdf.image(image_path, x=(210 - 120) / 2, w=120)  # 120 width, centered
                    pdf.ln(20)  # Add space after image
                else:
                    pdf.cell(0, 10, f'Image not found: {image_path}', ln=True)
                    pdf.ln(10)

        # Save the PDF report
        pdf.output(output_pdf_path)
        return f"Successfully created and saved the evaluation report at: {output_pdf_path}"

    except Exception as e:
        return f"Failed to create PDF report. Error: {repr(e)}"

