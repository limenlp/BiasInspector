import os
import json
import re
from typing import Annotated
import pandas as pd
from scipy import stats
import numpy as np
import seaborn as sns
from fpdf import FPDF
import matplotlib
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import matplotlib
import matplotlib.pyplot as plt
from langchain_experimental.utilities import PythonREPL
import math
from scipy.stats import chi2_contingency
matplotlib.use('Agg')



"""
tools.py

- load_csv_file: Loads a CSV file and returns it as a Pandas DataFrame.
- get_user_input_tool: Captures user input dynamically during an interaction and formats it as a dictionary to be added to the Agent's conversation.
"""

# ======================================
#
# - load_csv_file: Loads a CSV file and returns it as a Pandas DataFrame.
#   Input: file_path (str), Output: Pandas DataFrame (pd.DataFrame).
#
# - get_user_input_tool: Captures user input dynamically during an interaction and formats it as a dictionary to be added to the Agent's conversation.  
#   Input: None. Output: User input message (dict) or error message (str).
# 
# ======================================
    
@tool
def load_csv_file(
    file_path: Annotated[str, "The path to the CSV file to load."]
) -> pd.DataFrame:
    """
    Load a CSV file and return it as a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file to load.

    Returns:
        pd.DataFrame: The loaded data as a Pandas DataFrame, or an error message if the process failed.
    """
    try:
        # Load the CSV file
        df = pd.read_csv(file_path)
        return df
    
    except Exception as e:
        return f"Failed to load the CSV file. Error: {repr(e)}"


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

    
