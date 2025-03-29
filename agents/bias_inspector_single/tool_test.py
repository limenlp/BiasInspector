import os
import pandas as pd
from typing import Annotated
import seaborn as sns
from fpdf import FPDF
import numpy as np
from langchain_experimental.utilities import PythonREPL
import json
import sys
import pip
from scipy import stats
from scipy.stats import chi2_contingency

def tool(func):
    return func




@tool
def get_reference_method_by_id(
    references_file_path: Annotated[str, "The path to the JSON file containing the references data."],
    id_to_retrieve: Annotated[str, "The ID of the reference whose method needs to be retrieved."]
) -> dict:
    """
    Retrieve the method for a specific reference by ID from the references JSON file.

    Args:
        references_file_path (str): The path to the JSON file containing the references data, which is source_files/references.json
        id_to_retrieve (str): The ID of the reference for which the method needs to be retrieved.

    Returns:
        dict: The method corresponding to the given ID, or an error message if not found.
    """
    try:
        # Load the JSON file with UTF-8 encoding
        with open(references_file_path, 'r', encoding='utf-8') as file:
            references = json.load(file)
        
        # Find the reference with the given ID and return its method
        for ref in references:
            if ref["id"] == id_to_retrieve:
                method = ref["method"]
                # Return the method and the additional note as a single string
                return f"{method}\n\nYou need to generate executable code based on this method and call the execute_python_code function to execute it."
        
        return {"error": f"Method for reference ID {id_to_retrieve} not found."}

    except Exception as e:
        return {
            "error": f"Failed to retrieve method for reference ID {id_to_retrieve}. Error: {repr(e)}"
        }









def main():
    
    # Call the function to test
    result = get_reference_method_by_id(
        references_file_path="source_files/references.json",
        id_to_retrieve="A-0-1"
    )
    
    # Print the result
    print("Test Result:")
    print(result)

if __name__ == "__main__":
    main()
