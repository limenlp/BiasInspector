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

This file contains various utility functions, categorized into four groups:

1. Data Loading and Preprocessing Tools:
    - get_csv_features: Reads a CSV file and returns all feature names (column names).
    - load_csv_file: Loads a CSV file and returns it as a Pandas DataFrame.
    - extract_single_column: Extracts a single column from a CSV file and saves it as a new dataset.
    - extract_two_columns: Extracts two columns from a CSV file and saves them as a new dataset.
    - clean_missing_values: Cleans missing or invalid values from specified columns and saves the cleaned dataset.
    - normalize_or_standardize_data: Applies 'normalize' or 'standardize' to a specified column and saves the result as a new dataset.
    - group_and_aggregate: Groups the data by a specified column and applies an aggregation function on another column.

2. Detect and Analysis Tools:
    - categorical_distribution_shannon_balance: Analyzes the distribution bias of a categorical column using Shannon entropy and Balance metric
    - categorical_distribution_max_min_ratio: Analyzes the distribution bias of a categorical column using the max/min ratio of categories.   
    - categorical_distribution_entropy: Analyzes the distribution bias of a categorical column using Shannon entropy and normalized entropy.
    - categorical_distribution_gini: Analyzes the distribution bias of a categorical column using the Gini Index with Laplace smoothing and sample size correction.
    - categorical_distribution_relative_risk: Analyzes the distribution bias of a categorical column using relative risk by comparing observed and expected frequencies.
    - numerical_distribution_skewness: Analyzes the distribution bias of a numerical column using skewness to assess asymmetry in the data.
    - numerical_distribution_kurtosis: Analyzes the distribution bias of a numerical column using kurtosis to assess the "tailedness" of the distribution.
    - numerical_distribution_outlier: Analyzes the distribution bias of a numerical column using Z-score outlier detection to assess the percentage of outliers.
    - numerical_distribution_cohens_d_mad: Analyzes the distribution bias of a numerical column using Cohen's d, calculated with Median Absolute Deviation (MAD) for robustness against outliers.
    - numerical_distribution_quantile_deviation: Analyzes the distribution bias of a numerical column using quantile deviation, calculated as the ratio of Q3-Q2 to the interquartile range (IQR).
    - categorical_categorical_correlation_cramers_v: Analyzes the correlation bias between two categorical columns using Cramér's V, which measures association strength based on the chi-square statistic.
    - categorical_categorical_correlation_elift: Analyzes the correlation bias between two categorical columns using Elift, calculated as the ratio of confidence(X -> Y) to confidence(Y).
    - categorical_categorical_correlation_statistical_parity: Analyzes the correlation bias between two categorical columns using statistical parity and Z-scores to assess differences in proportions between groups.
    - categorical_categorical_correlation_lipschitz: Analyzes the correlation bias between two categorical columns using a Lipschitz function to measure distribution loss differences between groups.
    - categorical_categorical_correlation_total_variation: Analyzes the correlation bias between two categorical columns using Total Variation Distance (TVD) to measure the difference between group-specific and overall distributions.
    - categorical_numerical_correlation_max_abs_mean: Analyzes the correlation bias between a categorical and a numerical column by computing the standardized mean for each category and evaluating the maximum absolute mean (N value).
    - categorical_numerical_correlation_cohens_d: Analyzes the correlation bias between a categorical and a numerical column using Cohen's d to measure the effect size based on an independent t-test.
    - categorical_numerical_correlation_standardized_difference: Analyzes the correlation bias between a categorical and a numerical column using Standardized Difference (SD), calculated with mean and Median Absolute Deviation (MAD).
    - categorical_numerical_correlation_causal_effect: Analyzes the correlation bias between a categorical treatment and a numerical outcome using causal inference to estimate the Average Causal Effect (ACE).
    - categorical_numerical_correlation_pse: Analyzes the correlation bias between a categorical and a numerical column using Path-Specific Effect (PSE), along with the Average Direct Effect (ADE) and Average Indirect Effect (AIE).
    - numerical_numerical_correlation_pearson: Analyzes the correlation bias between two numerical columns using Pearson correlation to measure the strength of their linear relationship.
    - numerical_numerical_correlation_nmi: Analyzes the correlation bias between two numerical columns using Normalized Mutual Information (NMI) after discretizing the data into bins.
    - numerical_numerical_correlation_hgr_approximation: Analyzes the correlation bias between two numerical columns using HGR approximation and χ² divergence, combining Pearson correlation and Kernel Density Estimation (KDE) to assess the strength of the relationship.
    - numerical_numerical_correlation_wasserstein: Analyzes the correlation bias between two numerical columns using Wasserstein-2 distance to measure the differences between their distributions.
    - numerical_numerical_correlation_hsic: Analyzes the correlation bias between two numerical columns using the Hilbert-Schmidt Independence Criterion (HSIC) with Radial Basis Function (RBF) kernels to measure their dependence.

3. Visualization Tools:
    - plot_bar_chart: Generates a bar chart for a specified column in a CSV file and saves it as an image.
    - plot_pie_chart: Generates a pie chart for a specified column in a CSV file and saves it as an image. 
    - plot_horizontal_bar_chart: Generates a horizontal bar chart for a specified column in a CSV file and saves it as an image
    - plot_treemap: Generates a treemap for a specified column in a CSV file and saves it as an image. 
    - plot_heatmap: Generates a heatmap for the frequency distribution of a specified column in a CSV file and saves it as an image.
    - plot_correlation_heatmap: Generates a correlation heatmap for multiple specified columns in a CSV file and saves it as an image.
    - plot_stacked_bar_chart: Generates a stacked bar chart for two specified categorical columns in a CSV file and saves it as an image.
    - plot_grouped_bar_chart: Generates a grouped bar chart for two specified categorical columns in a CSV file and saves it as an image.
    - plot_box_plot: Generates a box plot for a categorical column and a numeric column in a CSV file and saves it as an image.

4. Miscellaneous Tools:
    - get_user_input_tool: Captures user input dynamically during an interaction and formats it as a dictionary to be added to the Agent's conversation.
    - get_all_reference_intentions: Retrieves all intentions from the references JSON file, including each reference's id and corresponding intention.
    - get_reference_method_by_id: Retrieves the method for a specific reference by ID from the references JSON file.  
    - generate_bias_report_pdf: Generates a bias detection report in PDF format, combining text and charts as specified in the input.
    - execute_python_code: Executes the provided Python code and returns the printed output, if any.
"""

# ======================================
# 1. Data Loading and Preprocessing Tools: 
#
# - get_csv_features: Reads a CSV file and returns all feature names (column names).
#   Input: file_path (str), Output: feature names (str).
#
# - load_csv_file: Loads a CSV file and returns it as a Pandas DataFrame.
#   Input: file_path (str), Output: Pandas DataFrame (pd.DataFrame).
#
# - extract_single_column: Extracts a single column from a CSV file and saves it as a new dataset.
#   Input: file_path (str), column_name (str), new_dataset_name (str), Output: Success message (str).
#
# - extract_two_columns: Extracts two columns from a CSV file and saves them as a new dataset.
#   Input: file_path (str), column1 (str), column2 (str), new_dataset_name (str), Output: Success message (str).
#
# - clean_missing_values: Cleans missing or invalid values from specified columns and saves the cleaned dataset.
#   Input: file_path (str), columns_to_check (list), new_dataset_name (str), Output: Success message (str).
#
# - normalize_or_standardize_data: Applies 'normalize' or 'standardize' to a specified column and saves the result as a new dataset.
#   Input: file_path (str), column_name (str), method (str), new_dataset_name (str), Output: Success message (str).
#
# - group_and_aggregate: Groups the data by a specified column and applies an aggregation function on another column.  
#   Input: file_path (str), group_by_column (str), aggregate_column (str), aggregation_method (str). Output: Aggregated data (str) or error message (str).
#
# ======================================

@tool
def get_csv_features(file_path: Annotated[str, "The path to the CSV file to read."]):
    """
    Read a CSV file and return all feature names (column names).

    Args:
        file_path (str): The path to the CSV file to read. Example: "example_test_.csv"

    Returns:
        str: A message indicating whether the CSV file was successfully read and listing all feature names,
             or an error message if the file could not be read.
    """
    try:
        df = pd.read_csv(file_path)
        features = df.columns.tolist()
        return (
            f"Successfully read the CSV file. The features are:\n{features}\n\n"
        )
    except Exception as e:
        return f"Failed to read the CSV file. Error: {repr(e)}"
    
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
def extract_single_column(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_name: Annotated[str, "The name of the column to extract."],
    new_dataset_name: Annotated[str, "The name of the new dataset to save."]
) -> str:
    """
    Extract a single column from a CSV file and save it as a new dataset.

    Args:
        file_path (str): The path to the CSV file to read (e.g., "path/to/data.csv").
        column_name (str): The name of the column to extract (e.g., "Age").
        new_dataset_name (str): The name of the new dataset file to save (without file extension) (e.g., "ages_dataset").

    Returns:
        str: A message indicating whether the column was successfully extracted and saved as a new dataset in the 
             "generated_files" directory, or an error message if the process failed. The new dataset file will be saved 
             as "generated_files/{new_dataset_name}.csv".

    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Check if the specified column exists in the DataFrame
        if column_name not in df.columns:
            return f"Error: Column {column_name} does not exist in the dataset."
        
        # Extract the specified column
        extracted_df = df[[column_name]]
        
        # Define the directory to save the new dataset
        data_directory = "generated_files"
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        
        # Save the new dataset to the specified directory
        new_filepath = os.path.join(data_directory, f"{new_dataset_name}.csv")
        extracted_df.to_csv(new_filepath, index=False)
        
        return f"Successfully created new dataset: {new_filepath}"
    
    except Exception as e:
        return f"Failed to extract column and create new dataset. Error: {repr(e)}"


@tool
def extract_two_columns(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column1: Annotated[str, "The name of the first column to extract."],
    column2: Annotated[str, "The name of the second column to extract."],
    new_dataset_name: Annotated[str, "The name of the new dataset to save."]
) -> str:
    """
    Extract two columns from a CSV file and save them as a new dataset.

    Args:
        file_path (str): The path to the CSV file to read (e.g., "path/to/data.csv").
        column1 (str): The name of the first column to extract (e.g., "Age").
        column2 (str): The name of the second column to extract (e.g., "Occupation").
        new_dataset_name (str): The name of the new dataset file to save (without file extension) (e.g., "age_occupation_dataset").

    Returns:
        str: A message indicating whether the columns were successfully extracted and saved as a new dataset in the 
             "generated_files" directory, or an error message if the process failed. The new dataset file will be saved 
             as "generated_files/{new_dataset_name}.csv".

    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Check if the specified columns exist in the DataFrame
        if column1 not in df.columns or column2 not in df.columns:
            return f"Error: Column {column1} or {column2} does not exist in the dataset."
        
        # Extract the specified columns
        extracted_df = df[[column1, column2]]
        
        # Define the directory to save the new dataset
        data_directory = "generated_files"
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        
        # Save the new dataset to the specified directory
        new_filepath = os.path.join(data_directory, f"{new_dataset_name}.csv")
        extracted_df.to_csv(new_filepath, index=False)
        
        return f"Successfully created new dataset: {new_filepath}"
    
    except Exception as e:
        return f"Failed to extract columns and create new dataset. Error: {repr(e)}"

@tool
def clean_missing_values(
    file_path: Annotated[str, "The path to the CSV file to read."],
    columns_to_check: Annotated[list, "List of column names to check for missing or invalid values."],
    new_dataset_name: Annotated[str, "The name of the new dataset to save after cleaning."]
) -> str:
    """
    Clean missing or invalid values from specified columns in a CSV file and save the cleaned dataset.

    Args:
        file_path (str): The path to the CSV file to read (e.g., "path/to/data.csv").
        columns_to_check (list): List of column names to check for missing or invalid values (e.g., ["Age", "Occupation"]).
        new_dataset_name (str): The name of the new dataset file to save after cleaning (without file extension) (e.g., "cleaned_data").

    Returns:
        str: A message indicating whether the cleaning process was successful and the new dataset was created in the 
            "generated_files" directory, or an error message if the process failed. The new dataset file will be saved 
            as "generated_files/{new_dataset_name}.csv".
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Check if the specified columns exist in the DataFrame
        missing_columns = [col for col in columns_to_check if col not in df.columns]
        if missing_columns:
            return f"Error: The following columns do not exist in the dataset: {', '.join(missing_columns)}"
        
        # Clean missing or invalid values (e.g., NaN)
        cleaned_df = df.dropna(subset=columns_to_check)
        
        # Define the directory to save the new dataset
        data_directory = "generated_files"
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        
        # Save the cleaned dataset to the specified directory
        new_filepath = os.path.join(data_directory, f"{new_dataset_name}.csv")
        cleaned_df.to_csv(new_filepath, index=False)
        
        return f"Successfully cleaned the dataset and created new dataset: {new_filepath}"
    
    except Exception as e:
        return f"Failed to clean the dataset. Error: {repr(e)}"

@tool
def normalize_or_standardize_data(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_name: Annotated[str, "The name of the column to normalize or standardize."],
    method: Annotated[str, "The method to apply: 'normalize' or 'standardize'."],
    new_dataset_name: Annotated[str, "The name of the new dataset to save."]
) -> str:
    """
    Normalize or standardize a specified column from a CSV file and save the result as a new dataset.

    Args:
        file_path (str): The path to the CSV file to read.
        column_name (str): The name of the column to normalize or standardize.
        method (str): The method to apply, either 'normalize' (scales data to range [0, 1]) or 'standardize' 
                      (scales data to have mean 0 and standard deviation 1).
        new_dataset_name (str): The name of the new dataset to save (without file extension).

    Returns:
        str: A message indicating whether the normalization or standardization was successful and the new dataset was created,
             or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Check if the specified column exists in the DataFrame
        if column_name not in df.columns:
            return f"Error: Column {column_name} does not exist in the dataset."
        
        # Normalize or standardize the column
        if method == 'normalize':
            df[column_name] = (df[column_name] - df[column_name].min()) / (df[column_name].max() - df[column_name].min())
        elif method == 'standardize':
            df[column_name] = (df[column_name] - df[column_name].mean()) / df[column_name].std()
        else:
            return "Error: Invalid method. Please specify 'normalize' or 'standardize'."
        
        # Define the directory to save the new dataset
        data_directory = "generated_files"
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)

        # Save the new dataset to the specified directory
        new_filepath = os.path.join(data_directory, f"{new_dataset_name}.csv")
        df.to_csv(new_filepath, index=False)

        return f"Successfully created new dataset with {method} applied to column '{column_name}': {new_filepath}"

    except Exception as e:
        return f"Failed to normalize or standardize the dataset. Error: {repr(e)}"

@tool
def group_and_aggregate(
    file_path: Annotated[str, "The path to the CSV file to read."],
    group_by_column: Annotated[str, "The name of the column to group by."],
    aggregate_column: Annotated[str, "The name of the column to aggregate."],
    aggregation_method: Annotated[str, "The aggregation method to apply (e.g., 'mean', 'sum', 'count')."]
) -> str:
    """
    Group data by a specified column, apply an aggregation function on another column, and return the result.

    Args:
        file_path (str): The path to the CSV file to read.
        group_by_column (str): The name of the column to group by.
        aggregate_column (str): The name of the column to aggregate.
        aggregation_method (str): The aggregation method to apply (e.g., 'mean', 'sum', 'count').

    Returns:
        str: The grouped and aggregated result or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified columns exist in the DataFrame
        if group_by_column not in df.columns or aggregate_column not in df.columns:
            return f"Error: Column {group_by_column} or {aggregate_column} does not exist in the dataset."

        # Group by the specified column and apply the aggregation method
        grouped_df = df.groupby(group_by_column).agg({aggregate_column: aggregation_method})

        # Convert the result to a string format for return
        return grouped_df.to_string()

    except Exception as e:
        return f"Failed to group and aggregate the dataset. Error: {repr(e)}"
   


# ======================================
# 2. Detect and Analysis Tools
#
# ============Detect Distribution Bias in a Categorical Features==========================
#
# - categorical_distribution_shannon_balance: Analyzes the distribution bias of a categorical column using Shannon entropy and Balance metric. 
#   Input: file_path (str), column_name (str). Output: A dictionary with Shannon entropy, balance metric, bias evaluation, or an error message (dict).
#
# - categorical_distribution_max_min_ratio: Analyzes the distribution bias of a categorical column using the max/min ratio of categories.  
#   Input: file_path (str), column_name (str). Output: A dictionary with the max/min ratio or an error message (dict).
#
# - categorical_distribution_entropy: Analyzes the distribution bias of a categorical column using Shannon entropy and normalized entropy.  
#   Input: file_path (str), column_name (str). Output: A dictionary with entropy, normalized entropy, bias evaluation, or an error message (dict).
#
# - categorical_distribution_gini: Analyzes the distribution bias of a categorical column using the Gini Index with Laplace smoothing and sample size correction.  
#   Input: file_path (str), column_name (str). Output: A dictionary with corrected and adjusted Gini Index, bias evaluation, or an error message (dict).
#
# - categorical_distribution_relative_risk: Analyzes the distribution bias of a categorical column using relative risk by comparing observed and expected frequencies.  
#   Input: file_path (str), column_name (str). Output: A dictionary with normalized bias score, relative risks for each category, or an error message (dict).
#
# ============Detect Distribution Bias in a Numerical Features==========================
#
# - numerical_distribution_skewness: Analyzes the distribution bias of a numerical column using skewness to assess asymmetry in the data.  
#   Input: file_path (str), column_name (str). Output: A dictionary with the skewness value, bias evaluation, or an error message (dict).
#
# - numerical_distribution_kurtosis: Analyzes the distribution bias of a numerical column using kurtosis to assess the "tailedness" of the distribution.  
#   Input: file_path (str), column_name (str). Output: A dictionary with the kurtosis value, bias evaluation, or an error message (dict).
#
# - numerical_distribution_outlier: Analyzes the distribution bias of a numerical column using Z-score outlier detection to assess the percentage of outliers.  
#   Input: file_path (str), column_name (str). Output: A dictionary with the outlier percentage, bias evaluation, or an error message (dict).
#
# - numerical_distribution_cohens_d_mad: Analyzes the distribution bias of a numerical column using Cohen's d, calculated with Median Absolute Deviation (MAD) for robustness against outliers.  
#   Input: file_path (str), column_name (str). Output: A dictionary with Cohen's d value, bias evaluation, or an error message (dict).
#
# - numerical_distribution_quantile_deviation: Analyzes the distribution bias of a numerical column using quantile deviation, calculated as the ratio of Q3-Q2 to the interquartile range (IQR).  
#   Input: file_path (str), column_name (str). Output: A dictionary with quantile deviation value, bias evaluation, or an error message (dict).
#
# ============Detect Correlation Bias in Two Categorical Features==========================
#
# - categorical_categorical_correlation_cramers_v: Analyzes the correlation bias between two categorical columns using Cramér's V, which measures association strength based on the chi-square statistic.  
#   Input: file_path (str), column_a (str), column_b (str). Output: A dictionary with the Cramér's V value, bias evaluation, or an error message (dict).
#
# - categorical_categorical_correlation_elift: Analyzes the correlation bias between two categorical columns using Elift, calculated as the ratio of confidence(X -> Y) to confidence(Y).  
#   Input: file_path (str), column_x (str), column_y (str). Output: A dictionary with the maximum Elift value, bias evaluation, or an error message (dict).
#
# - categorical_categorical_correlation_statistical_parity: Analyzes the correlation bias between two categorical columns using statistical parity and Z-scores to assess differences in proportions between groups.  
#   Input: file_path (str), column_x (str), column_y (str). Output: A dictionary with the maximum Z-value, bias evaluation, or an error message (dict).
#
# - categorical_categorical_correlation_lipschitz: Analyzes the correlation bias between two categorical columns using a Lipschitz function to measure distribution loss differences between groups.  
#   Input: file_path (str), column_x (str), column_y (str). Output: A dictionary with the maximum delta value, bias evaluation, or an error message (dict).
#
# - categorical_categorical_correlation_total_variation: Analyzes the correlation bias between two categorical columns using Total Variation Distance (TVD) to measure the difference between group-specific and overall distributions.  
#   Input: file_path (str), column_x (str), column_y (str). Output: A dictionary with the maximum TVD value, bias evaluation, or an error message (dict).
#
# ============Detect Correlation Bias in a Categorical Feature and a Numerical Feature==========================
#
# - categorical_numerical_correlation_max_abs_mean: Analyzes the correlation bias between a categorical and a numerical column by computing the standardized mean for each category and evaluating the maximum absolute mean (N value).  
#   Input: file_path (str), column_cat (str), column_num (str). Output: A dictionary with the maximum absolute N value, bias evaluation, or an error message (dict).
#
# - categorical_numerical_correlation_cohens_d: Analyzes the correlation bias between a categorical and a numerical column using Cohen's d to measure the effect size based on an independent t-test.  
#   Input: file_path (str), column_cat (str), column_num (str). Output: A dictionary with the Cohen's d effect size, bias evaluation, or an error message (dict).
#
# - categorical_numerical_correlation_standardized_difference: Analyzes the correlation bias between a categorical and a numerical column using Standardized Difference (SD), calculated with mean and Median Absolute Deviation (MAD).  
#   Input: file_path (str), column_cat (str), column_num (str). Output: A dictionary with the standardized difference for the first category, bias evaluation, or an error message (dict).
#
# - categorical_numerical_correlation_causal_effect: Analyzes the correlation bias between a categorical treatment and a numerical outcome using causal inference to estimate the Average Causal Effect (ACE).  
#   Input: file_path (str), column_cat (str), column_num (str). Output: A dictionary with the estimated ACE, bias evaluation, or an error message (dict).
#
# - categorical_numerical_correlation_pse: Analyzes the correlation bias between a categorical and a numerical column using Path-Specific Effect (PSE), along with the Average Direct Effect (ADE) and Average Indirect Effect (AIE).  
#   Input: file_path (str), column_cat (str), column_num (str). Output: A dictionary with the PSE value, bias evaluation, or an error message (dict).
#
# ============Detect Correlation Bias in Two Numerical Features==========================
#
# - numerical_numerical_correlation_pearson: Analyzes the correlation bias between two numerical columns using Pearson correlation to measure the strength of their linear relationship.  
#   Input: file_path (str), column_x (str), column_y (str). Output: A dictionary with the Pearson correlation coefficient (r), bias evaluation, or an error message (dict).
#
# - numerical_numerical_correlation_nmi: Analyzes the correlation bias between two numerical columns using Normalized Mutual Information (NMI) after discretizing the data into bins.  
#   Input: file_path (str), column_x (str), column_y (str), bins (int). Output: A dictionary with the NMI value, bias evaluation, or an error message (dict).
#
# - numerical_numerical_correlation_hgr_approximation: Analyzes the correlation bias between two numerical columns using HGR approximation and χ² divergence, combining Pearson correlation and Kernel Density Estimation (KDE) to assess the strength of the relationship.  
#   Input: file_path (str), column_x (str), column_y (str). Output: A dictionary with the normalized χ² divergence, bias evaluation, or an error message (dict).
#
# - numerical_numerical_correlation_wasserstein: Analyzes the correlation bias between two numerical columns using Wasserstein-2 distance to measure the differences between their distributions.  
#   Input: file_path (str), column_x (str), column_y (str). Output: A dictionary with the Wasserstein-2 distance, bias evaluation, or an error message (dict).
#
# - numerical_numerical_correlation_hsic: Analyzes the correlation bias between two numerical columns using the Hilbert-Schmidt Independence Criterion (HSIC) with Radial Basis Function (RBF) kernels to measure their dependence.  
#   Input: file_path (str), column_x (str), column_y (str), sigma (float). Output: A dictionary with the HSIC value, bias evaluation, or an error message (dict).
#
# ======================================


    
@tool
def categorical_distribution_shannon_balance(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_name: Annotated[str, "The name of the categorical column to analyze."]
) -> dict:
    """
    Perform distribution bias analysis on a categorical column using Shannon entropy and Balance metric.

    This method calculates Shannon entropy to measure the uncertainty (or information content) 
    of the categorical distribution, and the Balance metric to evaluate how evenly the categories 
    are distributed in the dataset.

    The bias is evaluated according to the Balance metric with the following thresholds:
        - Balance >= 0.95: Level 1
        - 0.80 <= Balance < 0.95: Level 2
        - 0.65 <= Balance < 0.80: Level 3
        - 0.50 <= Balance < 0.65: Level 4
        - Balance < 0.50: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_name (str): The name of the categorical column to analyze.

    Returns:
        dict: A dictionary containing the balance metric and Shannon entropy of the column,
              or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists in the DataFrame
        if column_name not in df.columns:
            return {"error": f"Error: Column {column_name} does not exist in the dataset."}

        # Handle missing values
        df = df.dropna(subset=[column_name])

        # Check if the column is categorical
        if pd.api.types.is_numeric_dtype(df[column_name]):
            return {"error": "Error: This tool is designed for categorical features only."}

        # Calculate the frequency of each category
        feature_counts = df[column_name].value_counts()
        total = len(df)

        # Compute Shannon entropy
        H = 0
        for count in feature_counts:
            probability = count / total
            H -= probability * math.log(probability, 2)

        # Number of categories
        k = df[column_name].nunique()

        # Calculate the balance metric
        if k > 1:
            Balance = H / math.log(k, 2)
        else:
            Balance = 0  # If only one category exists, balance metric is 0

        # Return the balance metric and entropy in a dictionary
        result = {
            'Balance': Balance,
            'Shannon_Entropy': H
        }

        return result

    except Exception as e:
        return {"error": f"Failed to perform distribution bias analysis. Error: {repr(e)}"}
    
@tool
def categorical_distribution_max_min_ratio(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_name: Annotated[str, "The name of the categorical column to analyze."]
) -> dict:
    """
    Perform max/min ratio distribution bias analysis on a specified categorical column.

    This method calculates the max/min ratio of categories using relative frequency for the 
    specified categorical feature in the dataset.

    The bias is evaluated according to the max/min ratio with the following thresholds:
        - Ratio > 100: Level 5
        - Ratio > 10: Level 4
        - Ratio > 5: Level 3
        - Ratio > 2: Level 2
        - Ratio <= 2: Level 1

    Args:
        file_path (str): The path to the CSV file to read.
        column_name (str): The name of the categorical column to analyze.

    Returns:
        dict: A dictionary where the key is the column name, and the value is the max/min ratio,
              or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists
        if column_name not in df.columns:
            return {"error": f"Column {column_name} does not exist in the dataset."}

        # Remove missing values
        df_feature = df.dropna(subset=[column_name])

        # Check if the column is categorical
        if pd.api.types.is_numeric_dtype(df[column_name]):
            return {"error": "The specified column is not categorical."}

        # Function to calculate max/min ratio
        def calculate_max_min_ratio(series):
            counts = series.value_counts(normalize=True)  # Use relative frequency
            max_ratio = counts.max()
            min_ratio = counts.min()
            # If the minimum category ratio is close to 0, treat it as a sign of extreme bias
            if min_ratio == 0:
                return float('inf')
            return max_ratio / min_ratio

        # Calculate the max/min ratio of the categories
        max_min_ratio = calculate_max_min_ratio(df_feature[column_name])

        # Return the result as a dictionary
        return {column_name: max_min_ratio}

    except Exception as e:
        return {"error": f"Failed to perform max/min ratio bias analysis. Error: {repr(e)}"}

@tool
def categorical_distribution_entropy(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_name: Annotated[str, "The name of the categorical column to analyze."]
) -> dict:
    """
    Perform distribution bias analysis on a specified categorical column using Shannon entropy.

    This method calculates Shannon entropy and normalized entropy to measure the uncertainty 
    (or information content) of the categorical distribution.

    The bias is evaluated according to the normalized entropy with the following thresholds:
        - Normalized Entropy >= 0.95: Level 1
        - 0.80 <= Normalized Entropy < 0.95: Level 2
        - 0.65 <= Normalized Entropy < 0.80: Level 3
        - 0.45 <= Normalized Entropy < 0.65: Level 4
        - Normalized Entropy < 0.45: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_name (str): The name of the categorical column to analyze.

    Returns:
        dict: A dictionary containing the entropy and normalized entropy,
              or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists
        if column_name not in df.columns:
            return {"error": f"Column {column_name} does not exist in the dataset."}

        # Handle missing values
        df_feature = df.dropna(subset=[column_name])

        # Check if the column is categorical
        if pd.api.types.is_numeric_dtype(df[column_name]):
            return {"error": "The specified column is not categorical."}

        # Calculate the frequency of each category
        feature_counts = df_feature[column_name].value_counts()
        total = len(df_feature)

        # Compute Shannon entropy
        entropy = 0
        for count in feature_counts:
            probability = count / total
            entropy -= probability * math.log(probability, 2)

        # Number of categories
        num_categories = df_feature[column_name].nunique()

        # Normalize entropy to get a normalized entropy metric
        if num_categories > 1:
            max_entropy = math.log(num_categories, 2)
            normalized_entropy = entropy / max_entropy
        else:
            normalized_entropy = 0  # If only one category exists, normalized entropy is 0


        # Return the result as a dictionary
        return {
            "Entropy": entropy,
            "Normalized_Entropy": normalized_entropy,
        }

    except Exception as e:
        return {"error": f"Failed to perform entropy-based bias analysis. Error: {repr(e)}"}
    
@tool
def categorical_distribution_gini(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_name: Annotated[str, "The name of the categorical column to analyze."]
) -> dict:
    """
    Perform distribution bias analysis on a specified categorical column using Gini Index.

    This method calculates the Gini Index with Laplace smoothing to avoid zero counts and 
    applies a sample size correction to the Gini Index. The adjusted Gini Index is then 
    compared to the theoretical maximum Gini Index to assess the distribution bias.

    The bias is evaluated according to the adjusted Gini Index with the following thresholds:
        - Adjusted Gini >= 0.95: Level 1
        - 0.80 <= Adjusted Gini < 0.95: Level 2
        - 0.65 <= Adjusted Gini < 0.80: Level 3
        - 0.40 <= Adjusted Gini < 0.65: Level 4
        - Adjusted Gini < 0.40: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_name (str): The name of the categorical column to analyze.
    

    Returns:
        dict: A dictionary containing the corrected Gini Index and adjusted Gini Index,
              or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists
        if column_name not in df.columns:
            return {"error": f"Column {column_name} does not exist in the dataset."}

        # Handle missing values
        df_feature = df.dropna(subset=[column_name])

        # Check if the column is categorical
        if pd.api.types.is_numeric_dtype(df[column_name]):
            return {"error": "The specified column is not categorical."}

        # Calculate the frequency of each category
        feature_counts = df_feature[column_name].value_counts()
        total = len(df_feature)

        # Apply Laplace smoothing to avoid zero counts
        smoothing_factor = 1  # A small smoothing factor to avoid zero counts
        smoothed_counts = (feature_counts + smoothing_factor) / (total + smoothing_factor * len(feature_counts))

        # Calculate Gini Index with smoothing
        gini_index = 1 - sum(smoothed_counts ** 2)

        # Apply sample size correction to the Gini Index calculation
        sample_correction = 1 / (total + 1e-5)  # Add a small value to avoid division by zero
        corrected_gini_index = gini_index * (1 - sample_correction)

        # Calculate the theoretical maximum Gini Index for the given number of categories
        max_gini = (len(feature_counts) - 1) / len(feature_counts)
        adjusted_gini = corrected_gini_index / max_gini

        # Return the result as a dictionary
        return {
            "Corrected_Gini_Index": corrected_gini_index,
            "Adjusted_Gini_Index": adjusted_gini
        }

    except Exception as e:
        return {"error": f"Failed to perform Gini-based bias analysis. Error: {repr(e)}"}
    
@tool
def categorical_distribution_relative_risk(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_name: Annotated[str, "The name of the categorical column to analyze."]
) -> dict:
    """
    Perform distribution bias analysis on a specified categorical column using relative risk.

    This method calculates the relative risks of each category by comparing their observed frequency
    with the expected frequency assuming uniform distribution. It then computes a normalized bias 
    score as the ratio of max relative risk to min relative risk.

    The bias is evaluated according to the normalized bias score with the following thresholds:
        - Normalized Bias Score >= 100: Level 5
        - 10 <= Normalized Bias Score < 100: Level 4
        - 3 <= Normalized Bias Score < 10: Level 3
        - 1.1 <= Normalized Bias Score < 3: Level 2
        - Normalized Bias Score <= 1.1: Level 1

    Args:
        file_path (str): The path to the CSV file to read.
        column_name (str): The name of the categorical column to analyze.

    Returns:
        dict: A dictionary containing the normalized bias score and relative risks for each category,
              or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists
        if column_name not in df.columns:
            return {"error": f"Column {column_name} does not exist in the dataset."}

        # Handle missing values
        df_feature = df.dropna(subset=[column_name])

        # Calculate the frequency of each category
        feature_counts = df_feature[column_name].value_counts(normalize=True)

        # Calculate the expected frequency assuming uniform distribution
        expected_frequency = 1 / len(feature_counts)

        # Calculate the relative risks
        relative_risks = feature_counts / expected_frequency

        # Compute the ratio of max relative risk to min relative risk
        max_relative_risk = relative_risks.max()
        min_relative_risk = relative_risks.min()

        # Calculate normalized bias score (ratio of max to min relative risk)
        normalized_bias_score = max_relative_risk / min_relative_risk if min_relative_risk > 0 else max_relative_risk

        # Return the relative risks and normalized bias score
        return {
            "Relative_Risks": relative_risks.to_dict(),
            "Normalized_Bias_Score": normalized_bias_score
        }

    except Exception as e:
        return {"error": f"Failed to perform relative risk bias analysis. Error: {repr(e)}"}
    
@tool
def numerical_distribution_skewness(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_name: Annotated[str, "The name of the numerical column to analyze."]
) -> dict:
    """
    Perform distribution bias analysis on a specified numerical column using skewness.

    This method calculates the skewness of the numerical column to assess the distribution bias. 
    Based on the skewness value, the bias is categorized into different levels:
        - Absolute Skewness < 0.5: Level 1
        - 0.5 <= Absolute Skewness < 0.8: Level 2
        - 0.8 <= Absolute Skewness < 0.9: Level 3
        - 0.9 <= Absolute Skewness < 1: Level 4
        - Absolute Skewness >= 1: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_name (str): The name of the numerical column to analyze.

    Returns:
        dict: A dictionary containing the skewness value of the column,
              or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists
        if column_name not in df.columns:
            return {"error": f"Column {column_name} does not exist in the dataset."}

        # Handle missing values
        df_feature = df.dropna(subset=[column_name])

        # Ensure the feature is numeric
        if not pd.api.types.is_numeric_dtype(df_feature[column_name]):
            return {"error": "The specified column is not a numeric feature."}

        # Calculate skewness
        skewness = df_feature[column_name].skew()

        # Return the skewness value
        return {
            "Skewness": skewness
        }

    except Exception as e:
        return {"error": f"Failed to perform skewness bias analysis. Error: {repr(e)}"}
    
@tool
def numerical_distribution_kurtosis(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_name: Annotated[str, "The name of the numerical column to analyze."]
) -> dict:
    """
    Perform distribution bias analysis on a specified numerical column using kurtosis.

    This method calculates the kurtosis of the numerical column to assess the distribution bias.
    Based on the kurtosis value, the bias is categorized into different levels:
        - Absolute Kurtosis < 0.3: Level 1
        - 0.3 <= Absolute Kurtosis < 0.6: Level 2
        - 0.6 <= Absolute Kurtosis < 0.9: Level 3
        - 0.9 <= Absolute Kurtosis < 1.2: Level 4
        - Absolute Kurtosis >= 1.2: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_name (str): The name of the numerical column to analyze.

    Returns:
        dict: A dictionary containing the kurtosis value of the column,
              or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists
        if column_name not in df.columns:
            return {"error": f"Column {column_name} does not exist in the dataset."}

        # Handle missing values
        df_feature = df.dropna(subset=[column_name])

        # Ensure the feature is numeric
        if not pd.api.types.is_numeric_dtype(df_feature[column_name]):
            return {"error": "The specified column is not a numeric feature."}

        # Calculate kurtosis
        kurtosis = df_feature[column_name].kurtosis()

        # Return the kurtosis value
        return {
            "Kurtosis": kurtosis
        }

    except Exception as e:
        return {"error": f"Failed to perform kurtosis bias analysis. Error: {repr(e)}"}

    
@tool
def numerical_distribution_outlier(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_name: Annotated[str, "The name of the numerical column to analyze."]
) -> dict:
    """
    Perform distribution bias analysis on a specified numerical column using Z-score outlier detection.

    This method calculates the Z-scores of the numerical column to identify outliers and determine the
    percentage of outliers in the data. Based on the outlier percentage, the bias is categorized into
    different levels:
        - Outlier Percentage < 0.5%: Level 1
        - 0.5% <= Outlier Percentage < 0.75%: Level 2
        - 0.75% <= Outlier Percentage < 0.90%: Level 3
        - 0.90% <= Outlier Percentage < 3%: Level 4
        - Outlier Percentage >= 3%: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_name (str): The name of the numerical column to analyze.

    Returns:
        dict: A dictionary containing the outlier percentage,
              or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists
        if column_name not in df.columns:
            return {"error": f"Column {column_name} does not exist in the dataset."}

        # Handle missing values
        df_feature = df.dropna(subset=[column_name])

        # Ensure the feature is numeric
        if not pd.api.types.is_numeric_dtype(df_feature[column_name]):
            return {"error": "The specified column is not a numeric feature."}

        # Calculate mean and standard deviation
        mean = df_feature[column_name].mean()
        std = df_feature[column_name].std()

        # Compute Z-scores
        z_scores = (df_feature[column_name] - mean) / std

        # Count how many Z-scores are outside the threshold (e.g., |Z| > 3)
        outliers = np.sum(np.abs(z_scores) > 3)
        total_points = len(df_feature[column_name])
        outlier_percentage = (outliers / total_points) * 100

        # Return the outlier percentage
        return {
            "Outlier_Percentage": outlier_percentage
        }

    except Exception as e:
        return {"error": f"Failed to perform outlier bias analysis. Error: {repr(e)}"}
    
@tool
def numerical_distribution_cohens_d_mad(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_name: Annotated[str, "The name of the numerical column to analyze."]
) -> dict:
    """
    Perform distribution bias analysis on a specified numerical column using Cohen's d,
    calculated with the Median Absolute Deviation (MAD) to reduce sensitivity to sample size.

    Cohen's d is a measure of effect size. This version uses MAD instead of standard deviation to 
    make the analysis less sensitive to outliers and sample size.
    Based on the Cohen's d value, the bias is categorized into different levels:
        - Absolute Cohen's d < 0.1: Level 1
        - 0.1 <= Absolute Cohen's d < 0.2: Level 2
        - 0.2 <= Absolute Cohen's d < 0.3: Level 3
        - 0.3 <= Absolute Cohen's d < 0.4: Level 4
        - Absolute Cohen's d >= 0.4: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_name (str): The name of the numerical column to analyze.

    Returns:
        dict: A dictionary containing the Cohen's d value,
              or an error message if the process failed.
    """

    def cohen_d_mad(data):
        """
        Calculate Cohen's d using Median Absolute Deviation (MAD) instead of standard deviation.
        """
        median_value = np.median(data)
        mad = np.median(np.abs(data - median_value))  # Median absolute deviation

        # If MAD is 0, add a small constant to avoid division by zero
        if mad == 0:
            mad = 1e-6  # Small constant

        mean_diff = np.mean(data) - median_value
        return mean_diff / mad

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists
        if column_name not in df.columns:
            return {"error": f"Column {column_name} does not exist in the dataset."}

        # Handle missing values
        df_feature = df.dropna(subset=[column_name])

        # Ensure the feature is numeric
        if not pd.api.types.is_numeric_dtype(df_feature[column_name]):
            return {"error": "The specified column is not a numeric feature."}

        # Calculate Cohen's d using MAD
        cohen_d_value = cohen_d_mad(df_feature[column_name])

        # Return the Cohen's d value
        return {
            "Cohen_d_MAD": cohen_d_value
        }

    except Exception as e:
        return {"error": f"Failed to perform Cohen's d bias analysis using MAD. Error: {repr(e)}"}

@tool
def numerical_distribution_quantile_deviation(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_name: Annotated[str, "The name of the numerical column to analyze."]
) -> dict:
    """
    Perform distribution bias analysis on a specified numerical column using quantile deviation.

    This method calculates the quantile deviation of the numerical column, defined as the ratio of 
    the difference between the third quartile (Q3) and the median (Q2) to the interquartile range (IQR).
    Based on the quantile deviation, the bias is categorized into different levels:
        - Absolute Quantile Deviation < 0.50: Level 1
        - 0.50 <= Absolute Quantile Deviation < 0.56: Level 2
        - 0.56 <= Absolute Quantile Deviation < 0.57: Level 3
        - 0.57 <= Absolute Quantile Deviation < 0.58: Level 4
        - Absolute Quantile Deviation >= 0.58: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_name (str): The name of the numerical column to analyze.

    Returns:
        dict: A dictionary containing the quantile deviation value,
              or an error message if the process failed.
    """

    def quantile_deviation(data):
        """
        Calculate quantile deviation as (Q3 - Q2) / IQR (Interquartile Range).
        """
        Q1 = np.percentile(data, 25)
        Q2 = np.percentile(data, 50)
        Q3 = np.percentile(data, 75)
        IQR = Q3 - Q1  # Interquartile Range
        return (Q3 - Q2) / IQR

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists
        if column_name not in df.columns:
            return {"error": f"Column {column_name} does not exist in the dataset."}

        # Handle missing values
        df_feature = df.dropna(subset=[column_name])

        # Ensure the feature is numeric
        if not pd.api.types.is_numeric_dtype(df_feature[column_name]):
            return {"error": "The specified column is not a numeric feature."}

        # Calculate quantile deviation
        q_dev = quantile_deviation(df_feature[column_name])

        # Return the quantile deviation value
        return {
            "Quantile_Deviation": q_dev
        }

    except Exception as e:
        return {"error": f"Failed to perform quantile deviation bias analysis. Error: {repr(e)}"}
    
@tool
def categorical_categorical_correlation_cramers_v(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_a: Annotated[str, "The name of the first categorical column."],
    column_b: Annotated[str, "The name of the second categorical column."]
) -> dict:
    """
    Perform correlation bias analysis on two specified categorical columns using Cramér's V.

    This method calculates Cramér's V to measure the association between two categorical variables
    based on the chi-square statistic. The bias is evaluated based on the Cramér's V value:
        - Cramér's V < 0.1: Level 1
        - 0.1 <= Cramér's V < 0.3: Level 2
        - 0.3 <= Cramér's V < 0.5: Level 3
        - 0.5 <= Cramér's V < 0.7: Level 4
        - Cramér's V >= 0.7: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_a (str): The name of the first categorical column.
        column_b (str): The name of the second categorical column.

    Returns:
        dict: A dictionary containing the Cramér's V value,
              or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified columns exist
        if column_a not in df.columns or column_b not in df.columns:
            return {"error": f"Columns {column_a} or {column_b} do not exist in the dataset."}

        # Check if both columns are categorical
        if not (pd.api.types.is_object_dtype(df[column_a]) or pd.api.types.is_categorical_dtype(df[column_a])):
            return {"error": f"'{column_a}' must be a categorical feature."}
        if not (pd.api.types.is_object_dtype(df[column_b]) or pd.api.types.is_categorical_dtype(df[column_b])):
            return {"error": f"'{column_b}' must be a categorical feature."}

        # Drop missing values
        df = df.dropna(subset=[column_a, column_b])

        # Create a contingency table
        contingency_table = pd.crosstab(df[column_a], df[column_b])

        # Check if the contingency table has sufficient data
        if contingency_table.size == 0:
            return {"error": "Contingency table is empty. Check your data."}

        # Perform chi-square test
        chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

        # Calculate Cramér's V
        n = contingency_table.sum().sum()
        if n == 0:
            cramer_v = 0
        else:
            min_dim = min(contingency_table.shape) - 1
            cramer_v = np.sqrt((chi2_stat / n) / min_dim) if min_dim > 0 else 0

        # Return only the Cramér's V value, not the bias level
        return {
            "Cramers_V": cramer_v
        }

    except Exception as e:
        return {"error": f"Failed to perform Cramér's V bias analysis. Error: {repr(e)}"}
    
@tool
def categorical_categorical_correlation_elift(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_x: Annotated[str, "The name of the first categorical column."],
    column_y: Annotated[str, "The name of the second categorical column."]
) -> dict:
    """
    Perform correlation bias analysis on two specified categorical columns using Elift.

    This method calculates the Elift value to measure the correlation between two categorical variables.
    Elift is calculated as the ratio of confidence(X -> Y) to confidence(Y). 
    Based on the maximum Elift value, the bias is categorized into different levels:
        - Max Elift <= 1.25: Level 1
        - 1.25 < Max Elift <= 1.5: Level 2
        - 1.5 < Max Elift <= 2.0: Level 3
        - 2.0 < Max Elift <= 2.5: Level 4
        - Max Elift > 2.5: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_x (str): The name of the first categorical column.
        column_y (str): The name of the second categorical column.

    Returns:
        dict: A dictionary containing the maximum Elift value,
              or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified columns exist
        if column_x not in df.columns or column_y not in df.columns:
            return {"error": f"Columns {column_x} or {column_y} do not exist in the dataset."}

        # Check if both columns are categorical
        if not (pd.api.types.is_object_dtype(df[column_x]) or pd.api.types.is_categorical_dtype(df[column_x])):
            return {"error": f"'{column_x}' must be a categorical feature."}
        if not (pd.api.types.is_object_dtype(df[column_y]) or pd.api.types.is_categorical_dtype(df[column_y])):
            return {"error": f"'{column_y}' must be a categorical feature."}

        # Drop missing values
        df = df.dropna(subset=[column_x, column_y])

        # Total number of records
        N = len(df)

        # Get the categories of feature X and Y
        categories_x = df[column_x].unique()
        categories_y = df[column_y].unique()

        # Initialize the list to store elift values
        elift_values = []

        # Calculate conf(Y)
        conf_y = df[column_y].value_counts(normalize=True).to_dict()

        # Iterate through all combinations of X and Y categories
        for x in categories_x:
            supp_x = len(df[df[column_x] == x]) / N  # supp(X)
            for y in categories_y:
                supp_y = len(df[df[column_y] == y]) / N  # supp(Y)
                supp_xy = len(df[(df[column_x] == x) & (df[column_y] == y)]) / N  # supp(X, Y)
                if supp_x == 0 or conf_y[y] == 0:
                    continue
                conf_x_to_y = supp_xy / supp_x  # conf(X -> Y)
                elift = conf_x_to_y / conf_y[y]  # elift(X -> Y)

                # Store the results
                elift_values.append({
                    'X': x,
                    'Y': y,
                    'support_X': supp_x,
                    'support_Y': supp_y,
                    'support_XY': supp_xy,
                    'confidence_X_to_Y': conf_x_to_y,
                    'conf_Y': conf_y[y],
                    'elift': elift
                })

        # Find the maximum elift value
        max_elift = max([item['elift'] for item in elift_values])

        # Return only the maximum Elift value, without bias level
        return {
            "Max_Elift": max_elift
        }

    except Exception as e:
        return {"error": f"Failed to perform Elift bias analysis. Error: {repr(e)}"}
    
@tool
def categorical_categorical_correlation_statistical_parity(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_x: Annotated[str, "The name of the first categorical column."],
    column_y: Annotated[str, "The name of the second categorical column."]
) -> dict:
    """
    Perform correlation bias analysis on two specified categorical columns using statistical parity and Z-scores.

    This method calculates the Z-scores for differences in proportions between groups defined by 
    feature X on feature Y, based on statistical parity. It measures if certain groups in feature X 
    have significantly different proportions for feature Y.
    Based on the Z-score, the bias is categorized into different levels:
        - Max Z-value <= 0.25: Level 1
        - 0.25 < Max Z-value <= 0.50: Level 2
        - 0.50 < Max Z-value <= 0.75: Level 3
        - 0.75 < Max Z-value <= 1.00: Level 4
        - Max Z-value > 1.00: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_x (str): The name of the first categorical column.
        column_y (str): The name of the second categorical column.

    Returns:
        dict: A dictionary containing the maximum Z-value,
              or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified columns exist
        if column_x not in df.columns or column_y not in df.columns:
            return {"error": f"Columns {column_x} or {column_y} do not exist in the dataset."}

        # Check if both columns are categorical
        if not (pd.api.types.is_object_dtype(df[column_x]) or pd.api.types.is_categorical_dtype(df[column_x])):
            return {"error": f"'{column_x}' must be a categorical feature."}
        if not (pd.api.types.is_object_dtype(df[column_y]) or pd.api.types.is_categorical_dtype(df[column_y])):
            return {"error": f"'{column_y}' must be a categorical feature."}

        # Drop missing values
        df = df.dropna(subset=[column_x, column_y])

        # Total number of records
        N = len(df)

        # Calculate overall proportion (mean)
        overall_proportion = df[column_y].value_counts(normalize=True).to_dict()

        # Initialize a list to store statistical parity values
        parity_values = []

        # Iterate through all categories of column_x
        for x_category in df[column_x].unique():
            group_df = df[df[column_x] == x_category]
            N_g = len(group_df)

            # Calculate group-specific proportion for column_y
            group_proportion = group_df[column_y].value_counts(normalize=True).to_dict()

            # Compute Z-scores to capture significant differences
            for y_category in df[column_y].unique():
                overall_mean = overall_proportion.get(y_category, 0)
                group_mean = group_proportion.get(y_category, 0)

                # Calculate Z-score: (group_mean - overall_mean) / stddev
                stddev = np.sqrt(np.mean((df[column_y] == y_category).astype(float)) * (1 - np.mean((df[column_y] == y_category).astype(float))) + 1e-6)
                if stddev == 0:
                    continue

                Z_value = (group_mean - overall_mean) / stddev

                # Store the results
                parity_values.append({
                    'X': x_category,
                    'Y': y_category,
                    'group_mean': group_mean,
                    'overall_mean': overall_mean,
                    'Z_value': Z_value
                })

        # Find the maximum absolute Z_value
        max_Z_value = max([abs(item['Z_value']) for item in parity_values])

        # Return only the maximum Z-value, without bias level
        return {
            "Max_Z_value": max_Z_value
        }

    except Exception as e:
        return {"error": f"Failed to perform statistical parity bias analysis. Error: {repr(e)}"}
    
@tool
def categorical_categorical_correlation_lipschitz(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_x: Annotated[str, "The name of the first categorical column."],
    column_y: Annotated[str, "The name of the second categorical column."]
) -> dict:
    """
    Perform correlation bias analysis on two specified categorical columns using a Lipschitz function.

    This method calculates the bias between two categorical features using a continuous Lipschitz function
    to assess the loss differences between the group-specific distributions of feature Y given feature X,
    compared to the overall distribution of feature Y. The bias is evaluated using the delta values calculated
    for each group.
    
    Based on the maximum delta value, the bias is categorized into different levels:
        - Max delta <= 0.25: Level 1
        - 0.25 < Max delta <= 0.50: Level 2
        - 0.50 < Max delta <= 0.75: Level 3
        - 0.75 < Max delta <= 1.00: Level 4
        - Max delta > 1.00: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_x (str): The name of the first categorical column.
        column_y (str): The name of the second categorical column.

    Returns:
        dict: A dictionary containing the maximum delta value,
              or an error message if the process failed.
    """
    try:
        # Step 1: Read the CSV file
        df = pd.read_csv(file_path)

        # Ensure there are two categorical features
        if column_x not in df.columns or column_y not in df.columns:
            return {"error": f"Columns {column_x} or {column_y} do not exist in the dataset."}

        # Check if both columns are categorical
        if not (pd.api.types.is_object_dtype(df[column_x]) or pd.api.types.is_categorical_dtype(df[column_x])):
            return {"error": f"'{column_x}' must be a categorical feature."}
        if not (pd.api.types.is_object_dtype(df[column_y]) or pd.api.types.is_categorical_dtype(df[column_y])):
            return {"error": f"'{column_y}' must be a categorical feature."}

        # Drop missing values
        df = df.dropna(subset=[column_x, column_y])

        # Step 1: Set the weighted loss function for each categorical group
        overall_loss = df[column_y].value_counts(normalize=True).to_dict()

        # Initialize a list to store results
        results = []

        # Step 2: Define the overall loss function for each group
        for x_category in df[column_x].unique():
            group_df = df[df[column_x] == x_category]
            group_loss = group_df[column_y].value_counts(normalize=True).to_dict()

            # Step 3: Use a continuous Lipschitz function to represent the loss differences, f(l) = sum(sqrt(l_k))
            for y_category in df[column_y].unique():
                overall_mean = overall_loss.get(y_category, 0)
                group_mean = group_loss.get(y_category, 0)

                # Step 4: Calculate the difference between the group loss and the overall mean loss Δ = (l_G - l) / σ
                stddev = np.sqrt(np.mean((df[column_y] == y_category).astype(float)) * (1 - np.mean((df[column_y] == y_category).astype(float))) + 1e-6)
                if stddev == 0:
                    continue

                delta = (group_mean - overall_mean) / stddev

                # Store the results for analysis
                results.append({
                    'X': x_category,
                    'Y': y_category,
                    'group_mean': group_mean,
                    'overall_mean': overall_mean,
                    'delta': delta
                })

        # Step 5: Set a threshold to assess the significance of the bias
        max_delta = max([abs(result['delta']) for result in results])

        # Return only the maximum delta value, without bias level
        return {
            "Max_Delta": max_delta
        }

    except Exception as e:
        return {"error": f"Failed to perform Lipschitz bias analysis. Error: {repr(e)}"}
    
@tool
def categorical_categorical_correlation_total_variation(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_x: Annotated[str, "The name of the first categorical column."],
    column_y: Annotated[str, "The name of the second categorical column."]
) -> dict:
    """
    Perform correlation bias analysis on two specified categorical columns using Total Variation Distance.

    This method calculates the Total Variation Distance (TVD) between the overall distribution of feature Y 
    and the group-specific distributions of feature Y, given feature X. It measures how different the 
    group distributions are from the overall distribution.
    
    Based on the maximum TVD, the bias is categorized into different levels:
        - Max TVD <= 0.1: Level 1
        - 0.1 < Max TVD <= 0.2: Level 2
        - 0.2 < Max TVD <= 0.3: Level 3
        - 0.3 < Max TVD <= 0.4: Level 4
        - Max TVD > 0.4: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_x (str): The name of the first categorical column.
        column_y (str): The name of the second categorical column.

    Returns:
        dict: A dictionary containing the maximum Total Variation Distance,
              or an error message if the process failed.
    """
    
    def total_variation_distance(p1, p2):
        """
        Calculate the Total Variation Distance between two distributions.
        """
        return 0.5 * np.sum(np.abs(p1 - p2))

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified columns exist
        if column_x not in df.columns or column_y not in df.columns:
            return {"error": f"Columns {column_x} or {column_y} do not exist in the dataset."}

        # Check if both columns are categorical
        if not (pd.api.types.is_object_dtype(df[column_x]) or pd.api.types.is_categorical_dtype(df[column_x])):
            return {"error": f"'{column_x}' must be a categorical feature."}
        if not (pd.api.types.is_object_dtype(df[column_y]) or pd.api.types.is_categorical_dtype(df[column_y])):
            return {"error": f"'{column_y}' must be a categorical feature."}

        # Drop missing values
        df = df.dropna(subset=[column_x, column_y])

        # Initialize a list to store Total Variation Distances
        tv_distances = []

        # Overall distribution of column_y
        overall_distribution = df[column_y].value_counts(normalize=True).sort_index()

        # Iterate through each category in column_x
        for x_category in df[column_x].unique():
            # Subset for this category
            subset = df[df[column_x] == x_category]

            # Distribution of column_y for this subset
            subset_distribution = subset[column_y].value_counts(normalize=True).sort_index()

            # Align distributions for consistent comparison
            subset_distribution = subset_distribution.reindex(overall_distribution.index, fill_value=0)

            # Calculate Total Variation Distance between the overall distribution and the group distribution
            tv_distance = total_variation_distance(overall_distribution.values, subset_distribution.values)
            tv_distances.append({
                'X': x_category,
                'Total Variation Distance': tv_distance
            })

        # Find the maximum Total Variation Distance
        max_tv_distance = max([item['Total Variation Distance'] for item in tv_distances])

        # Return only the maximum Total Variation Distance, without bias level
        return {
            "Max_Total_Variation_Distance": max_tv_distance
        }

    except Exception as e:
        return {"error": f"Failed to perform Total Variation Distance bias analysis. Error: {repr(e)}"}
    
@tool
def categorical_numerical_correlation_max_abs_mean(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_cat: Annotated[str, "The name of the categorical column."],
    column_num: Annotated[str, "The name of the numerical column."]
) -> dict:
    """
    Perform correlation bias analysis between a categorical and a numerical feature.

    This method calculates the correlation between one categorical feature and one numerical feature by 
    standardizing the numerical feature and computing the mean for each category. The bias is then determined
    by analyzing the maximum absolute mean (N value) for each category after standardization.
    
    Based on the maximum absolute N value, the bias is categorized into different levels:
        - Max |N| < 0.1: Level 1
        - 0.1 <= Max |N| < 0.2: Level 2
        - 0.2 <= Max |N| < 0.3: Level 3
        - 0.3 <= Max |N| < 0.4: Level 4
        - Max |N| >= 0.4: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_cat (str): The name of the categorical column.
        column_num (str): The name of the numerical column.

    Returns:
        dict: A dictionary containing the maximum absolute N value,
              or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Ensure the specified columns exist
        if column_cat not in df.columns or column_num not in df.columns:
            return {"error": f"Columns {column_cat} or {column_num} do not exist in the dataset."}

        # Check if the categorical and numerical columns are of correct types
        if not (pd.api.types.is_object_dtype(df[column_cat]) or pd.api.types.is_categorical_dtype(df[column_cat])):
            return {"error": f"'{column_cat}' must be a categorical feature."}
        if not pd.api.types.is_numeric_dtype(df[column_num]):
            return {"error": f"'{column_num}' must be a numerical feature."}

        # Drop rows with missing values in the relevant columns
        df = df.dropna(subset=[column_cat, column_num])

        # Check if the dataframe is empty after dropping NaNs
        if df.empty:
            return {"error": "No valid data after removing rows with missing values."}

        # Standardize the numerical feature
        df[column_num] = (df[column_num] - df[column_num].mean()) / df[column_num].std(ddof=0)

        # Get unique categories
        categories = df[column_cat].unique()

        # Calculate N values for each category
        N_values = []
        for category in categories:
            group = df[df[column_cat] == category][column_num]
            group_mean = group.mean()  # Since data is standardized, this is effectively the z-score
            N_values.append(group_mean)

        # Find the maximum absolute N value
        max_abs_N = max(abs(N) for N in N_values)

        # Return the maximum absolute N value
        return {
            "Max_Absolute_N_Value": max_abs_N
        }

    except Exception as e:
        return {"error": f"Failed to perform correlation bias analysis. Error: {repr(e)}"}
    
@tool
def categorical_numerical_correlation_cohens_d(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_cat: Annotated[str, "The name of the categorical column."],
    column_num: Annotated[str, "The name of the numerical column."]
) -> dict:
    """
    Perform correlation bias analysis between a categorical and a numerical feature using Cohen's d.

    This method calculates the correlation between one categorical feature and one numerical feature by 
    performing an independent t-test and calculating Cohen's d to determine the effect size. The bias is then
    assessed based on the effect size.
    
    Based on the Cohen's d value, the bias is categorized into different levels:
        - Cohen's d < 0.25: Level 1
        - 0.25 <= Cohen's d < 0.5: Level 2
        - 0.5 <= Cohen's d < 0.75: Level 3
        - 0.75 <= Cohen's d < 1.0: Level 4
        - Cohen's d >= 1.0: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_cat (str): The name of the categorical column (must have exactly two categories).
        column_num (str): The name of the numerical column.

    Returns:
        dict: A dictionary containing the Cohen's d effect size,
              or an error message if the process failed.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Ensure the specified columns exist
        if column_cat not in df.columns or column_num not in df.columns:
            return {"error": f"Columns {column_cat} or {column_num} do not exist in the dataset."}

        # Check if the categorical and numerical columns are of correct types
        if not (pd.api.types.is_object_dtype(df[column_cat]) or pd.api.types.is_categorical_dtype(df[column_cat])):
            return {"error": f"'{column_cat}' must be a categorical feature."}
        if not pd.api.types.is_numeric_dtype(df[column_num]):
            return {"error": f"'{column_num}' must be a numerical feature."}

        # Drop rows with missing values
        df = df.dropna(subset=[column_cat, column_num])

        # Get unique categories
        categories = df[column_cat].unique()
        num_categories = len(categories)

        # Ensure exactly two categories
        if num_categories != 2:
            return {"error": "The categorical feature must have exactly two categories."}

        # Get data for each category
        group1 = df[df[column_cat] == categories[0]][column_num]
        group2 = df[df[column_cat] == categories[1]][column_num]

        # Perform t-test
        stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)

        # Calculate Cohen's d
        s1 = np.var(group1, ddof=1)
        s2 = np.var(group2, ddof=1)
        s_pooled = np.sqrt((s1 + s2) / 2)  # Adjust pooled standard deviation to remove sample size dependency
        if s_pooled == 0:
            effect_size = 0
        else:
            d = (np.mean(group1) - np.mean(group2)) / s_pooled
            effect_size = abs(d)

        # Return the Cohen's d effect size
        return {
            "Cohens_d_Effect_Size": effect_size
        }

    except Exception as e:
        return {"error": f"Failed to perform correlation bias analysis using Cohen's d. Error: {repr(e)}"}

    
@tool
def categorical_numerical_correlation_standardized_difference(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_cat: Annotated[str, "The name of the categorical column."],
    column_num: Annotated[str, "The name of the numerical column."]
) -> dict:
    """
    Perform correlation bias analysis between a categorical and a numerical feature using Standardized Difference (SD).

    This method calculates the mean and Median Absolute Deviation (MAD) of the numerical feature grouped by the
    categorical feature. It then computes the standardized difference for each group, which is used to evaluate 
    the bias between categories.

    Based on the standardized difference, the bias is categorized into different levels:
        - |SD| < 0.1: Level 1
        - 0.1 <= |SD| < 0.3: Level 2
        - 0.3 <= |SD| < 0.5: Level 3
        - 0.5 <= |SD| < 0.7: Level 4
        - |SD| >= 0.7: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_cat (str): The name of the categorical column.
        column_num (str): The name of the numerical column.

    Returns:
        dict: A dictionary containing the standardized difference for the first category,
              or an error message if the process failed.
    """

    def calculate_mad(series):
        """Calculate Median Absolute Deviation (MAD)"""
        median = series.median()
        mad = np.median(np.abs(series - median))
        return mad

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Ensure the specified columns exist
        if column_cat not in df.columns or column_num not in df.columns:
            return {"error": f"Columns {column_cat} or {column_num} do not exist in the dataset."}

        # Check if the categorical and numerical columns are of correct types
        if not (pd.api.types.is_object_dtype(df[column_cat]) or pd.api.types.is_categorical_dtype(df[column_cat])):
            return {"error": f"'{column_cat}' must be a categorical feature."}
        if not pd.api.types.is_numeric_dtype(df[column_num]):
            return {"error": f"'{column_num}' must be a numerical feature."}

        # Drop rows with missing values in the relevant columns
        df = df.dropna(subset=[column_cat, column_num])

        # Step 1: Calculate the mean and std for the numerical feature by category
        grouped_stats = df.groupby(column_cat)[column_num].agg(['mean', 'std']).reset_index()

        # Step 2: Calculate overall mean for the numerical feature
        overall_mean = df[column_num].mean()

        # Step 3: Calculate Standardized Difference (SD) using a robust standard deviation (MAD)
        robust_std = calculate_mad(df[column_num])  # Manually calculating MAD

        grouped_stats['Standardized_Difference'] = (grouped_stats['mean'] - overall_mean) / robust_std

        # Step 4: Return the standardized difference for the first category
        if len(grouped_stats) < 1:
            return {"error": "No categories found."}

        # Return the standardized difference for the first category
        first_category_sd = grouped_stats['Standardized_Difference'].iloc[0]

        return {
            "Standardized_Difference_First_Category": first_category_sd
        }

    except Exception as e:
        return {"error": f"Failed to perform correlation bias analysis. Error: {repr(e)}"}
    
@tool
def categorical_numerical_correlation_causal_effect(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_cat: Annotated[str, "The name of the categorical column."],
    column_num: Annotated[str, "The name of the numerical column."]
) -> dict:
    """
    Perform correlation bias analysis between a categorical and a numerical feature using causal inference.

    This method uses the DoWhy causal inference library to estimate the causal effect of a categorical treatment 
    on a numerical outcome, based on the backdoor criterion. The bias is evaluated by calculating the Average 
    Causal Effect (ACE) between the two features.

    Based on the ACE value, the bias is categorized into different levels:
        - |ACE| < 1: Level 1
        - 1 <= |ACE| < 3: Level 2
        - 3 <= |ACE| < 6: Level 3
        - 6 <= |ACE| < 9: Level 4
        - |ACE| >= 9: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_cat (str): The name of the categorical column (treatment).
        column_num (str): The name of the numerical column (outcome).

    Returns:
        dict: A dictionary containing the estimated Average Causal Effect (ACE),
              or an error message if the process failed.
    """
    import pandas as pd
    import dowhy
    import warnings
    import contextlib
    import io

    # Suppress FutureWarnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Ensure the specified columns exist
        if column_cat not in df.columns or column_num not in df.columns:
            return {"error": f"Columns {column_cat} or {column_num} do not exist in the dataset."}

        # Check if the categorical and numerical columns are of correct types
        if not (pd.api.types.is_object_dtype(df[column_cat]) or pd.api.types.is_categorical_dtype(df[column_cat])):
            return {"error": f"'{column_cat}' must be a categorical feature."}
        if not pd.api.types.is_numeric_dtype(df[column_num]):
            return {"error": f"'{column_num}' must be a numerical feature."}

        # Drop rows with missing values in the relevant columns
        df = df.dropna(subset=[column_cat, column_num])

        # Convert the categorical feature to numerical encoding if necessary
        if not pd.api.types.is_numeric_dtype(df[column_cat]):
            df[column_cat] = pd.Categorical(df[column_cat]).codes

        # Step 1: Create a Causal Model using DoWhy
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            model = dowhy.CausalModel(
                data=df,
                treatment=column_cat,
                outcome=column_num,
                common_causes=[]  # No common causes provided in this case
            )

            # Step 2: Identify the causal effect
            identified_estimand = model.identify_effect()

            # Step 3: Estimate the causal effect using linear regression
            estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")

        # Step 4: Output the estimated effect
        ace_value = estimate.value

        # Return the Average Causal Effect (ACE)
        return {
            "Average_Causal_Effect_ACE": ace_value
        }

    except Exception as e:
        return {"error": f"Failed to perform causal effect analysis. Error: {repr(e)}"}
    
@tool
def categorical_numerical_correlation_pse(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_cat: Annotated[str, "The name of the categorical column."],
    column_num: Annotated[str, "The name of the numerical column."]
) -> dict:
    """
    Perform correlation bias analysis between a categorical and a numerical feature using Path-Specific Effect (PSE).

    This method calculates the Average Direct Effect (ADE), Average Indirect Effect (AIE), and Path-Specific Effect (PSE)
    to measure the correlation bias between one categorical and one numerical feature. The analysis is limited to
    categorical features with exactly two categories.

    Based on the PSE value, the bias is categorized into different levels:
        - PSE < 3: Level 1
        - 3 <= PSE < 4.5: Level 2
        - 4.5 <= PSE < 6: Level 3
        - 6 <= PSE < 7.5: Level 4
        - PSE >= 7.5: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_cat (str): The name of the categorical column.
        column_num (str): The name of the numerical column.

    Returns:
        dict: A dictionary containing the Path-Specific Effect (PSE),
              or an error message if the process failed.
    """
    import pandas as pd
    import numpy as np

    # Function to calculate Average Direct Effect (ADE)
    def calculate_ADE(group1, group2):
        mu_group1 = np.mean(group1)
        mu_group2 = np.mean(group2)
        ADE = mu_group1 - mu_group2
        return ADE

    # Function to calculate Average Indirect Effect (AIE)
    def calculate_AIE(group1, group2):
        var_group1 = np.var(group1, ddof=1)
        var_group2 = np.var(group2, ddof=1)
        AIE = var_group2 - var_group1  # Indirect effect is the difference in variances
        return AIE

    # Function to calculate Path-Specific Effect (PSE)
    def calculate_PSE(ADE, AIE):
        PSE = ADE + np.abs(AIE)  # Use absolute AIE to capture indirect effect
        return PSE

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Ensure the specified columns exist
        if column_cat not in df.columns or column_num not in df.columns:
            return {"error": f"Columns {column_cat} or {column_num} do not exist in the dataset."}

        # Check if the categorical and numerical columns are of correct types
        if not (pd.api.types.is_object_dtype(df[column_cat]) or pd.api.types.is_categorical_dtype(df[column_cat])):
            return {"error": f"'{column_cat}' must be a categorical feature."}
        if not pd.api.types.is_numeric_dtype(df[column_num]):
            return {"error": f"'{column_num}' must be a numerical feature."}

        # Drop rows with missing values in the relevant columns
        df = df.dropna(subset=[column_cat, column_num])

        # Get unique categories and check if there are exactly two categories
        categories = df[column_cat].unique()
        if len(categories) != 2:
            return {"error": "This tool supports only two categories in the categorical feature."}

        # Get data for each category
        group1 = df[df[column_cat] == categories[0]][column_num]
        group2 = df[df[column_cat] == categories[1]][column_num]

        # Step 2: Calculate ADE (Average Direct Effect)
        ADE = calculate_ADE(group1, group2)

        # Step 3: Calculate AIE (Average Indirect Effect)
        AIE = calculate_AIE(group1, group2)

        # Step 4: Calculate Path-Specific Effect (PSE)
        PSE = calculate_PSE(ADE, AIE)

        # Return the Path-Specific Effect (PSE)
        return {
            "Path_Specific_Effect": PSE
        }

    except Exception as e:
        return {"error": f"Failed to perform correlation bias analysis. Error: {repr(e)}"}
    
@tool
def numerical_numerical_correlation_pearson(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_x: Annotated[str, "The name of the first numerical column."],
    column_y: Annotated[str, "The name of the second numerical column."]
) -> dict:
    """
    Perform correlation bias analysis between two numerical features using Pearson correlation.

    This method calculates the Pearson correlation coefficient between two numerical features
    to measure their correlation. Based on the absolute value of the correlation coefficient, 
    the bias is categorized into different levels:
        - |r| < 0.2: Level 1
        - 0.2 <= |r| < 0.4: Level 2
        - 0.4 <= |r| < 0.6: Level 3
        - 0.6 <= |r| < 0.8: Level 4
        - |r| >= 0.8: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_x (str): The name of the first numerical column.
        column_y (str): The name of the second numerical column.

    Returns:
        dict: A dictionary containing the Pearson correlation coefficient (r),
              or an error message if the process failed.
    """
    import pandas as pd
    from scipy.stats import pearsonr

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Ensure the specified columns exist
        if column_x not in df.columns or column_y not in df.columns:
            return {"error": f"Columns {column_x} or {column_y} do not exist in the dataset."}

        # Check if both columns are numerical
        if not pd.api.types.is_numeric_dtype(df[column_x]):
            return {"error": f"'{column_x}' must be a numerical feature."}
        if not pd.api.types.is_numeric_dtype(df[column_y]):
            return {"error": f"'{column_y}' must be a numerical feature."}

        # Drop rows with missing values in the relevant columns
        df = df.dropna(subset=[column_x, column_y])

        # Extract numerical data
        x = df[column_x]
        y = df[column_y]

        # Calculate Pearson correlation coefficient and p-value
        r_value, p_value = pearsonr(x, y)
        abs_r = abs(r_value)

        # Return the Pearson correlation coefficient
        return {
            "Pearson_Correlation_Coefficient": abs_r
        }

    except Exception as e:
        return {"error": f"Failed to perform correlation bias analysis. Error: {repr(e)}"}
    
@tool
def numerical_numerical_correlation_nmi(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_x: Annotated[str, "The name of the first numerical column."],
    column_y: Annotated[str, "The name of the second numerical column."],
    bins: Annotated[int, "The number of bins to use for discretization."] = 10
) -> dict:
    """
    Perform correlation bias analysis between two numerical features using Normalized Mutual Information (NMI).

    This method calculates the Normalized Mutual Information (NMI) between two numerical features by first discretizing
    them into bins. The NMI measures the mutual dependence between the two features, and its value ranges from 0 to 1.

    Based on the NMI value, the bias is categorized into different levels:
        - NMI < 0.1: Level 1
        - 0.1 <= NMI < 0.3: Level 2
        - 0.3 <= NMI < 0.5: Level 3
        - 0.5 <= NMI < 0.7: Level 4
        - NMI >= 0.7: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_x (str): The name of the first numerical column.
        column_y (str): The name of the second numerical column.
        bins (int): The number of bins to use for discretization (default is 10).

    Returns:
        dict: A dictionary containing the Normalized Mutual Information (NMI),
              or an error message if the process failed.
    """
    import pandas as pd
    import numpy as np
    from sklearn.metrics import normalized_mutual_info_score

    def compute_normalized_mutual_information(x, y, bins=10):
        """Compute normalized mutual information after discretizing the numerical features."""
        # Discretize x and y into bins
        x_binned = np.digitize(x, np.linspace(min(x), max(x), bins))
        y_binned = np.digitize(y, np.linspace(min(y), max(y), bins))

        # Calculate normalized mutual information
        nmi = normalized_mutual_info_score(x_binned, y_binned)
        return nmi

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Ensure the specified columns exist
        if column_x not in df.columns or column_y not in df.columns:
            return {"error": f"Columns {column_x} or {column_y} do not exist in the dataset."}

        # Check if both columns are numerical
        if not pd.api.types.is_numeric_dtype(df[column_x]):
            return {"error": f"'{column_x}' must be a numerical feature."}
        if not pd.api.types.is_numeric_dtype(df[column_y]):
            return {"error": f"'{column_y}' must be a numerical feature."}

        # Drop rows with missing values in the relevant columns
        df = df.dropna(subset=[column_x, column_y])

        # Extract numerical data
        x = df[column_x]
        y = df[column_y]

        # Calculate normalized mutual information
        nmi = compute_normalized_mutual_information(x, y, bins)

        # Return the Normalized Mutual Information (NMI)
        return {
            "Normalized_Mutual_Information": nmi
        }

    except Exception as e:
        return {"error": f"Failed to perform correlation bias analysis. Error: {repr(e)}"}
    
@tool
def numerical_numerical_correlation_hgr_approximation(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_x: Annotated[str, "The name of the first numerical column."],
    column_y: Annotated[str, "The name of the second numerical column."]
) -> dict:
    """
    Perform correlation bias analysis between two numerical features using HGR approximation and χ² divergence.

    This method first approximates the Hirschfeld-Gebelein-Rényi (HGR) maximal correlation using Pearson correlation
    and then applies Kernel Density Estimation (KDE) to compute joint and marginal distributions. It calculates the 
    normalized χ² divergence to assess the strength of the bias between two numerical features.
    
    Based on the normalized χ² divergence value, the bias is categorized into different levels:
        - χ² < 0.1: Level 1
        - 0.1 <= χ² < 0.3: Level 2
        - 0.3 <= χ² < 0.5: Level 3
        - 0.5 <= χ² < 0.7: Level 4
        - χ² >= 0.7: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_x (str): The name of the first numerical column.
        column_y (str): The name of the second numerical column.

    Returns:
        dict: A dictionary containing the normalized χ² divergence,
              or an error message if the process failed.
    """
    import pandas as pd
    import numpy as np
    from scipy.stats import pearsonr
    from sklearn.neighbors import KernelDensity

    def calculate_pearson_correlation(x, y):
        """Calculate Pearson correlation as an approximation for linear correlation."""
        pearson_corr, _ = pearsonr(x, y)
        return pearson_corr

    def estimate_distribution(x, y):
        """Estimate joint and marginal distributions using Kernel Density Estimation."""
        xy = np.vstack([x, y]).T
        kde_joint = KernelDensity(kernel='gaussian', bandwidth=0.1).fit(xy)
        log_joint_density = kde_joint.score_samples(xy)
        joint_density = np.exp(log_joint_density)

        # Marginal distributions
        kde_x = KernelDensity(kernel='gaussian', bandwidth=1000).fit(x.reshape(-1, 1))
        kde_y = KernelDensity(kernel='gaussian', bandwidth=1000).fit(y.reshape(-1, 1))

        log_marginal_x_density = kde_x.score_samples(x.reshape(-1, 1))
        log_marginal_y_density = kde_y.score_samples(y.reshape(-1, 1))

        marginal_x_density = np.exp(log_marginal_x_density)
        marginal_y_density = np.exp(log_marginal_y_density)

        return joint_density, marginal_x_density, marginal_y_density

    def calculate_chi_square_divergence(joint_density, marginal_x_density, marginal_y_density):
        """Calculate normalized χ² divergence."""
        chi_square_divergence = np.sum((joint_density - marginal_x_density * marginal_y_density) ** 2)
        normalization_factor = np.sum(joint_density) + 1e-10
        normalized_chi_square = chi_square_divergence / normalization_factor
        return normalized_chi_square

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Ensure the specified columns exist
        if column_x not in df.columns or column_y not in df.columns:
            return {"error": f"Columns {column_x} or {column_y} do not exist in the dataset."}

        # Check if both columns are numerical
        if not pd.api.types.is_numeric_dtype(df[column_x]):
            return {"error": f"'{column_x}' must be a numerical feature."}
        if not pd.api.types.is_numeric_dtype(df[column_y]):
            return {"error": f"'{column_y}' must be a numerical feature."}

        # Drop rows with missing values in the relevant columns
        df = df.dropna(subset=[column_x, column_y])

        # Extract numerical data
        x = df[column_x].values
        y = df[column_y].values

        # Step 1 & 2: Calculate Pearson correlation (approximate HGR)
        pearson_corr = calculate_pearson_correlation(x, y)

        # Step 3 & 4: Estimate joint and marginal distributions using KDE
        joint_density, marginal_x_density, marginal_y_density = estimate_distribution(x, y)

        # Step 5: Calculate χ² divergence and normalize
        chi_square_value = calculate_chi_square_divergence(joint_density, marginal_x_density, marginal_y_density)

        # Return the normalized χ² divergence
        return {
            "Normalized_Chi_Square_Divergence": chi_square_value
        }

    except Exception as e:
        return {"error": f"Failed to perform correlation bias analysis. Error: {repr(e)}"}
    
@tool
def numerical_numerical_correlation_wasserstein(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_x: Annotated[str, "The name of the first numerical column."],
    column_y: Annotated[str, "The name of the second numerical column."]
) -> dict:
    """
    Perform correlation bias analysis between two numerical features using Wasserstein-2 distance.

    This method standardizes the two numerical features and calculates the Wasserstein-2 distance between them 
    without normalization by variance or sample size. Based on the Wasserstein distance value, the bias is categorized
    into different levels:
        - Wasserstein distance < 0.0001: Level 5
        - 0.0001 <= Wasserstein distance < 0.001: Level 4
        - 0.001 <= Wasserstein distance < 0.01: Level 3
        - 0.01 <= Wasserstein distance < 0.02: Level 2
        - Wasserstein distance >= 0.02: Level 1

    Args:
        file_path (str): The path to the CSV file to read.
        column_x (str): The name of the first numerical column.
        column_y (str): The name of the second numerical column.

    Returns:
        dict: A dictionary containing the Wasserstein-2 distance,
              or an error message if the process failed.
    """
    import pandas as pd
    import numpy as np
    from scipy.stats import wasserstein_distance
    from sklearn.preprocessing import StandardScaler

    def standardize_features(x, y):
        """Standardize numerical features using StandardScaler."""
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x.reshape(-1, 1)).flatten()
        y_scaled = scaler.fit_transform(y.reshape(-1, 1)).flatten()
        return x_scaled, y_scaled

    def calculate_wasserstein_distance(x, y):
        """Calculate Wasserstein-2 distance without normalization."""
        w_distance = wasserstein_distance(x, y)
        return w_distance

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Ensure the specified columns exist
        if column_x not in df.columns or column_y not in df.columns:
            return {"error": f"Columns {column_x} or {column_y} do not exist in the dataset."}

        # Check if both columns are numerical
        if not pd.api.types.is_numeric_dtype(df[column_x]):
            return {"error": f"'{column_x}' must be a numerical feature."}
        if not pd.api.types.is_numeric_dtype(df[column_y]):
            return {"error": f"'{column_y}' must be a numerical feature."}

        # Drop rows with missing values in the relevant columns
        df = df.dropna(subset=[column_x, column_y])

        # Extract numerical data
        x = df[column_x].values
        y = df[column_y].values

        # Standardize the features
        x_scaled, y_scaled = standardize_features(x, y)

        # Calculate Wasserstein-2 distance
        wasserstein_value = calculate_wasserstein_distance(x_scaled, y_scaled)

        # Return the Wasserstein-2 distance
        return {
            "Wasserstein_2_Distance": wasserstein_value
        }

    except Exception as e:
        return {"error": f"Failed to perform correlation bias analysis. Error: {repr(e)}"}
    
@tool
def numerical_numerical_correlation_hsic(
    file_path: Annotated[str, "The path to the CSV file to read."],
    column_x: Annotated[str, "The name of the first numerical column."],
    column_y: Annotated[str, "The name of the second numerical column."],
    sigma: Annotated[float, "The kernel bandwidth parameter for RBF."] = 1.0
) -> dict:
    """
    Perform correlation bias analysis between two numerical features using Hilbert-Schmidt Independence Criterion (HSIC).

    This method standardizes the two numerical features and calculates the Hilbert-Schmidt Independence Criterion (HSIC)
    using Radial Basis Function (RBF) kernels. HSIC measures the dependence between two random variables. It is 
    normalized by the sample size to reduce the impact of sample size. 
    
    Based on the HSIC value, the bias is categorized into different levels:
        - HSIC < 0.001: Level 1
        - 0.001 <= HSIC < 0.01: Level 2
        - 0.01 <= HSIC < 0.02: Level 3
        - 0.02 <= HSIC < 0.03: Level 4
        - HSIC >= 0.03: Level 5

    Args:
        file_path (str): The path to the CSV file to read.
        column_x (str): The name of the first numerical column.
        column_y (str): The name of the second numerical column.
        sigma (float): The kernel bandwidth parameter for RBF (default is 1.0).

    Returns:
        dict: A dictionary containing the HSIC value,
              or an error message if the process failed.
    """
    import pandas as pd
    import numpy as np
    from sklearn.metrics.pairwise import rbf_kernel

    def standardize_features(x, y):
        """Standardize features by subtracting their means and dividing by standard deviation."""
        x_standardized = (x - np.mean(x)) / np.std(x)
        y_standardized = (y - np.mean(y)) / np.std(y)
        return x_standardized, y_standardized

    def compute_hsic(x, y, sigma=1.0):
        """Compute the Hilbert-Schmidt Independence Criterion (HSIC) using RBF kernels with sample size normalization."""
        # Compute RBF kernel matrices for x and y
        Kx = rbf_kernel(x.reshape(-1, 1), gamma=1/(2*sigma**2))
        Ky = rbf_kernel(y.reshape(-1, 1), gamma=1/(2*sigma**2))

        # Centering matrix
        n = Kx.shape[0]
        H = np.eye(n) - np.ones((n, n)) / n

        # Center the kernel matrices
        Kx_centered = H @ Kx @ H
        Ky_centered = H @ Ky @ H

        # Compute the HSIC value
        hsic_value = np.trace(Kx_centered @ Ky_centered)

        # Normalize by sample size to reduce the impact of sample size
        hsic_value /= (n - 1) ** 2

        return hsic_value

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Ensure the specified columns exist
        if column_x not in df.columns or column_y not in df.columns:
            return {"error": f"Columns {column_x} or {column_y} do not exist in the dataset."}

        # Check if both columns are numerical
        if not pd.api.types.is_numeric_dtype(df[column_x]):
            return {"error": f"'{column_x}' must be a numerical feature."}
        if not pd.api.types.is_numeric_dtype(df[column_y]):
            return {"error": f"'{column_y}' must be a numerical feature."}

        # Drop rows with missing values in the relevant columns
        df = df.dropna(subset=[column_x, column_y])

        # Extract numerical data
        x = df[column_x].values
        y = df[column_y].values

        # Standardize features
        x_standardized, y_standardized = standardize_features(x, y)

        # Compute HSIC using RBF kernel with sample size normalization
        hsic_value = compute_hsic(x_standardized, y_standardized, sigma)

        # Return the HSIC value
        return {
            "HSIC_Value": hsic_value
        }

    except Exception as e:
        return {"error": f"Failed to perform correlation bias analysis. Error: {repr(e)}"}


# ======================================
# 3. Visualization Tools
#
# - plot_bar_chart: Generates a bar chart for a specified column in a CSV file and saves it as an image.  
#   Input: file_path (str), column_name (str), output_image_path (str). Output: Success message (str) or error message (str).
#
# - plot_pie_chart: Generates a pie chart for a specified column in a CSV file and saves it as an image.  
#   Input: file_path (str), column_name (str), output_image_path (str). Output: Success message (str) or error message (str).
#
# - plot_horizontal_bar_chart: Generates a horizontal bar chart for a specified column in a CSV file and saves it as an image.  
#   Input: file_path (str), column_name (str), output_image_path (str). Output: Success message (str) or error message (str).
#
# - plot_treemap: Generates a treemap for a specified column in a CSV file and saves it as an image.  
#   Input: file_path (str), column_name (str), output_image_path (str). Output: Success message (str) or error message (str).
#
# - plot_heatmap: Generates a heatmap for the frequency distribution of a specified column in a CSV file and saves it as an image.  
#   Input: file_path (str), column_name (str), output_image_path (str). Output: Success message (str) or error message (str).
#
# - plot_correlation_heatmap: Generates a correlation heatmap for multiple specified columns in a CSV file and saves it as an image.  
#   Input: file_path (str), columns (list[str]), output_image_path (str). Output: Success message (str) or error message (str).
#
# - plot_stacked_bar_chart: Generates a stacked bar chart for two specified categorical columns in a CSV file and saves it as an image.  
#   Input: file_path (str), column1 (str), column2 (str), output_image_path (str). Output: Success message (str) or error message (str).
#
# - plot_grouped_bar_chart: Generates a grouped bar chart for two specified categorical columns in a CSV file and saves it as an image.  
#   Input: file_path (str), column1 (str), column2 (str), output_image_path (str). Output: Success message (str) or error message (str).
#
# - plot_box_plot: Generates a box plot for a categorical column and a numeric column in a CSV file and saves it as an image.  
#   Input: file_path (str), category_column (str), numeric_column (str), output_image_path (str). Output: Success message (str) or error message (str).
#
# ====================================== 

@tool
def plot_bar_chart(
    file_path: Annotated[str, "The path to the CSV file containing the data."],
    column_name: Annotated[str, "The name of the single column to plot as a bar chart."],
    output_image_path: Annotated[str, "The path to save the bar chart image."]
) -> str:
    """
    Plot a bar chart for a specified single column in a CSV file and save the plot as an image.

    Args:
        file_path (str): The path to the CSV file containing the data.
        column_name (str): The name of the single column to plot as a bar chart.
        output_image_path (str): The path to save the bar chart image.

    Returns:
        str: A message indicating whether the bar chart was successfully created and saved,
             or an error message if the process failed.
    """

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists in the DataFrame
        if column_name not in df.columns:
            return f"Error: Column {column_name} does not exist in the dataset."

        # Set the seaborn theme for a cleaner aesthetic
        sns.set_theme(style="whitegrid")

        # Plot the bar chart for the single column
        plt.figure(figsize=(10, 6))
        ax = sns.countplot(x=column_name, data=df, palette="viridis")
        
        # Add title and labels with larger font sizes
        plt.title(f"Bar Chart of {column_name}", fontsize=18)
        plt.xlabel(f'{column_name}', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        
        # Add data labels to each bar (formatted as integers)
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', fontsize=12, color='black', xytext=(0, 5),
                        textcoords='offset points')

        # Remove the top and right spines for a cleaner look
        sns.despine()

        # Save the plot
        plt.savefig(output_image_path, bbox_inches='tight')
        plt.close()

        return f"Successfully created and saved the bar chart at: {output_image_path}"

    except Exception as e:
        return f"Failed to create and save bar chart. Error: {repr(e)}"


@tool
def plot_pie_chart(
    file_path: Annotated[str, "The path to the CSV file containing the data."],
    column_name: Annotated[str, "The name of the single column to plot as a pie chart."],
    output_image_path: Annotated[str, "The path to save the pie chart image."]
) -> str:
    """
    Plot a pie chart for a specified single column in a CSV file and save the plot as an image.

    Args:
        file_path (str): The path to the CSV file containing the data.
        column_name (str): The name of the single column to plot as a pie chart.
        output_image_path (str): The path to save the pie chart image.

    Returns:
        str: A message indicating whether the pie chart was successfully created and saved,
             or an error message if the process failed.
    """

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists in the DataFrame
        if column_name not in df.columns:
            return f"Error: Column {column_name} does not exist in the dataset."

        # Calculate the frequency of each category in the column
        counts = df[column_name].value_counts()

        # Generate a color palette with different colors for each section
        colors = sns.color_palette("viridis", len(counts))

        # Plot the pie chart for the single column with different colors
        plt.figure(figsize=(8, 8))
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
        
        # Add title
        plt.title(f"Pie Chart of {column_name}", fontsize=18)

        # Save the plot
        plt.savefig(output_image_path, bbox_inches='tight')
        plt.close()

        return f"Successfully created and saved the pie chart at: {output_image_path}"

    except Exception as e:
        return f"Failed to create and save pie chart. Error: {repr(e)}"

@tool
def plot_horizontal_bar_chart(
    file_path: Annotated[str, "The path to the CSV file containing the data."],
    column_name: Annotated[str, "The name of the single column to plot as a horizontal bar chart."],
    output_image_path: Annotated[str, "The path to save the horizontal bar chart image."]
) -> str:
    """
    Plot a horizontal bar chart for a specified single column in a CSV file and save the plot as an image.

    Args:
        file_path (str): The path to the CSV file containing the data.
        column_name (str): The name of the single column to plot as a horizontal bar chart.
        output_image_path (str): The path to save the horizontal bar chart image.

    Returns:
        str: A message indicating whether the horizontal bar chart was successfully created and saved,
             or an error message if the process failed.
    """
    import matplotlib
    matplotlib.use('Agg')  # Use Agg backend for saving images
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists in the DataFrame
        if column_name not in df.columns:
            return f"Error: Column {column_name} does not exist in the dataset."

        # Calculate the frequency of each category in the column
        counts = df[column_name].value_counts()

        # Generate a color palette with different colors for each bar
        colors = sns.color_palette("viridis", len(counts))

        # Plot the horizontal bar chart
        plt.figure(figsize=(10, 6))
        counts.plot(kind='barh', color=colors)
        
        # Add title and labels
        plt.title(f"Horizontal Bar Chart of {column_name}", fontsize=18)
        plt.xlabel('Count', fontsize=14)
        plt.ylabel(column_name, fontsize=14)

        # Save the plot
        plt.savefig(output_image_path, bbox_inches='tight')
        plt.close()

        return f"Successfully created and saved the horizontal bar chart at: {output_image_path}"

    except Exception as e:
        return f"Failed to create and save horizontal bar chart. Error: {repr(e)}"

@tool
def plot_treemap(
    file_path: Annotated[str, "The path to the CSV file containing the data."],
    column_name: Annotated[str, "The name of the single column to plot as a treemap."],
    output_image_path: Annotated[str, "The path to save the treemap image."]
) -> str:
    """
    Plot a treemap for a specified single column in a CSV file and save the plot as an image.

    Args:
        file_path (str): The path to the CSV file containing the data.
        column_name (str): The name of the single column to plot as a treemap.
        output_image_path (str): The path to save the treemap image.

    Returns:
        str: A message indicating whether the treemap was successfully created and saved,
             or an error message if the process failed.
    """
    import matplotlib
    matplotlib.use('Agg')  # Use Agg backend for saving images
    import matplotlib.pyplot as plt
    import pandas as pd
    import squarify
    import seaborn as sns

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists in the DataFrame
        if column_name not in df.columns:
            return f"Error: Column {column_name} does not exist in the dataset."

        # Calculate the frequency of each category in the column
        counts = df[column_name].value_counts()

        # Generate a color palette with different colors for each section of the treemap
        colors = sns.color_palette("viridis", len(counts))

        # Plot the treemap
        plt.figure(figsize=(10, 6))
        squarify.plot(sizes=counts.values, label=counts.index, alpha=.8, color=colors)
        
        # Add title
        plt.title(f"Treemap of {column_name}", fontsize=18)

        # Save the plot
        plt.axis('off')  # Turn off axis since it's a treemap
        plt.savefig(output_image_path, bbox_inches='tight')
        plt.close()

        return f"Successfully created and saved the treemap at: {output_image_path}"

    except Exception as e:
        return f"Failed to create and save treemap. Error: {repr(e)}"
    
@tool
def plot_heatmap(
    file_path: Annotated[str, "The path to the CSV file containing the data."],
    column_name: Annotated[str, "The name of the single column to plot as a heatmap."],
    output_image_path: Annotated[str, "The path to save the heatmap image."]
) -> str:
    """
    Plot a heatmap for the frequency distribution of a specified single column in a CSV file
    and save the plot as an image.

    Args:
        file_path (str): The path to the CSV file containing the data.
        column_name (str): The name of the single column to plot as a heatmap.
        output_image_path (str): The path to save the heatmap image.

    Returns:
        str: A message indicating whether the heatmap was successfully created and saved,
             or an error message if the process failed.
    """
    import matplotlib
    matplotlib.use('Agg')  # Use Agg backend for saving images
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists in the DataFrame
        if column_name not in df.columns:
            return f"Error: Column {column_name} does not exist in the dataset."

        # Calculate the frequency of each category in the column
        counts = df[column_name].value_counts().to_frame().T

        # Plot the heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(counts, annot=True, cmap="Blues", cbar=True, linewidths=0.5)
        
        # Add title
        plt.title(f"Heatmap of {column_name} Frequency", fontsize=18)

        # Save the plot
        plt.savefig(output_image_path, bbox_inches='tight')
        plt.close()

        return f"Successfully created and saved the heatmap at: {output_image_path}"

    except Exception as e:
        return f"Failed to create and save heatmap. Error: {repr(e)}"

@tool
def plot_correlation_heatmap(
    file_path: Annotated[str, "The path to the CSV file containing the data."],
    columns: Annotated[list[str], "The list of columns to include in the heatmap."],
    output_image_path: Annotated[str, "The path to save the heatmap image."]
) -> str:
    """
    Plot a correlation heatmap for multiple specified columns in a CSV file and save the plot as an image.

    Args:
        file_path (str): The path to the CSV file containing the data.
        columns (list[str]): The list of columns to include in the heatmap.
        output_image_path (str): The path to save the heatmap image.

    Returns:
        str: A message indicating whether the heatmap was successfully created and saved,
             or an error message if the process failed.
    """
    import matplotlib
    matplotlib.use('Agg')  # Use Agg backend for saving images
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified columns exist in the DataFrame
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            return f"Error: Columns {', '.join(missing_cols)} do not exist in the dataset."

        # Calculate the correlation matrix
        corr_matrix = df[columns].corr()

        # Plot the correlation heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5)

        # Add title
        plt.title("Correlation Heatmap", fontsize=18)

        # Save the plot
        plt.savefig(output_image_path, bbox_inches='tight')
        plt.close()

        return f"Successfully created and saved the correlation heatmap at: {output_image_path}"

    except Exception as e:
        return f"Failed to create and save heatmap. Error: {repr(e)}"

@tool
def plot_stacked_bar_chart(
    file_path: Annotated[str, "The path to the CSV file containing the data."],
    column1: Annotated[str, "The name of the first categorical column."],
    column2: Annotated[str, "The name of the second categorical column."],
    output_image_path: Annotated[str, "The path to save the stacked bar chart image."]
) -> str:
    """
    Plot a stacked bar chart for two specified categorical columns in a CSV file
    and save the plot as an image.

    Args:
        file_path (str): The path to the CSV file containing the data.
        column1 (str): The name of the first categorical column.
        column2 (str): The name of the second categorical column.
        output_image_path (str): The path to save the stacked bar chart image.

    Returns:
        str: A message indicating whether the stacked bar chart was successfully created and saved,
             or an error message if the process failed.
    """
    import matplotlib
    matplotlib.use('Agg')  # Use Agg backend for saving images
    import matplotlib.pyplot as plt
    import pandas as pd

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified columns exist in the DataFrame
        if column1 not in df.columns or column2 not in df.columns:
            return f"Error: Columns {column1} or {column2} do not exist in the dataset."

        # Create a crosstab (contingency table) between the two categorical columns
        crosstab = pd.crosstab(df[column1], df[column2], normalize='index')

        # Plot the stacked bar chart
        crosstab.plot(kind='bar', stacked=True, figsize=(10, 6), colormap="viridis")

        # Add title and labels
        plt.title(f'Stacked Bar Chart of {column1} vs {column2}', fontsize=18)
        plt.xlabel(column1, fontsize=14)
        plt.ylabel('Proportion', fontsize=14)
        plt.legend(title=column2, bbox_to_anchor=(1.05, 1), loc='upper left')

        # Save the plot
        plt.savefig(output_image_path, bbox_inches='tight')
        plt.close()

        return f"Successfully created and saved the stacked bar chart at: {output_image_path}"

    except Exception as e:
        return f"Failed to create and save stacked bar chart. Error: {repr(e)}"
    
@tool
def plot_grouped_bar_chart(
    file_path: Annotated[str, "The path to the CSV file containing the data."],
    column1: Annotated[str, "The name of the first categorical column."],
    column2: Annotated[str, "The name of the second categorical column (used as grouping)."],
    output_image_path: Annotated[str, "The path to save the grouped bar chart image."]
) -> str:
    """
    Plot a grouped bar chart for two specified categorical columns in a CSV file
    and save the plot as an image.

    Args:
        file_path (str): The path to the CSV file containing the data.
        column1 (str): The name of the first categorical column.
        column2 (str): The name of the second categorical column (used for grouping).
        output_image_path (str): The path to save the grouped bar chart image.

    Returns:
        str: A message indicating whether the grouped bar chart was successfully created and saved,
             or an error message if the process failed.
    """
    import matplotlib
    matplotlib.use('Agg')  # Use Agg backend for saving images
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified columns exist in the DataFrame
        if column1 not in df.columns or column2 not in df.columns:
            return f"Error: Columns {column1} or {column2} do not exist in the dataset."

        # Plot the grouped bar chart
        plt.figure(figsize=(10, 6))
        sns.countplot(x=column1, hue=column2, data=df, palette="Set2")

        # Add title and labels
        plt.title(f'Grouped Bar Chart of {column1} grouped by {column2}', fontsize=18)
        plt.xlabel(column1, fontsize=14)
        plt.ylabel('Count', fontsize=14)
        plt.legend(title=column2)

        # Save the plot
        plt.savefig(output_image_path, bbox_inches='tight')
        plt.close()

        return f"Successfully created and saved the grouped bar chart at: {output_image_path}"

    except Exception as e:
        return f"Failed to create and save grouped bar chart. Error: {repr(e)}"

@tool
def plot_box_plot(
    file_path: Annotated[str, "The path to the CSV file containing the data."],
    category_column: Annotated[str, "The name of the categorical column."],
    numeric_column: Annotated[str, "The name of the numeric column."],
    output_image_path: Annotated[str, "The path to save the box plot image."]
) -> str:
    """
    Plot a box plot for a categorical column and a numeric column in a CSV file
    and save the plot as an image.

    Args:
        file_path (str): The path to the CSV file containing the data.
        category_column (str): The name of the categorical column.
        numeric_column (str): The name of the numeric column.
        output_image_path (str): The path to save the box plot image.

    Returns:
        str: A message indicating whether the box plot was successfully created and saved,
             or an error message if the process failed.
    """

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified columns exist in the DataFrame
        if category_column not in df.columns or numeric_column not in df.columns:
            return f"Error: Columns {category_column} or {numeric_column} do not exist in the dataset."

        # Plot the box plot
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=category_column, y=numeric_column, data=df)
        plt.title(f'Box Plot of {numeric_column} grouped by {category_column}', fontsize=18)
        plt.xlabel(category_column, fontsize=14)
        plt.ylabel(numeric_column, fontsize=14)

        # Check if output_image_path has a file extension, if not, add .png
        if not os.path.splitext(output_image_path)[1]:
            output_image_path += ".png"

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)

        # Save the plot
        plt.savefig(output_image_path, bbox_inches='tight')
        plt.close()

        return f"Successfully created and saved the box plot at: {output_image_path}"

    except Exception as e:
        return f"Failed to create and save box plot. Error: {repr(e)}"


# ======================================
# 4. Miscellaneous Tools
# - get_user_input_tool: Captures user input dynamically during an interaction and formats it as a dictionary to be added to the Agent's conversation.  
#   Input: None. Output: User input message (dict) or error message (str).
#
# - read_reference_literature: Reads all reference literature files (text and PDF) from the specified folder and returns their content or a summary.  
#   Input: None. Output: Content or summary of reference literature (str) or error message (str).
#
# - get_all_reference_intentions: Retrieves all intentions from the references JSON file, including each reference's id and corresponding intention.  
#   Input: references_file_path (str). Output: List of dictionaries containing 'id' and 'intention', or an error message (str).
#
# - get_reference_method_by_id: Retrieves the method for a specific reference by ID from the references JSON file.  
#   Input: references_file_path (str), id_to_retrieve (int). Output: A dictionary containing the method for the given ID, or an error message (str) if not found.
#
# - generate_bias_report_pdf: Generates a bias detection report in PDF format, combining text and charts as specified in the input.  
#   Input: content_sections (list[dict]), output_pdf_path (str). Output: Success message (str) or error message (str).
#
# - execute_python_code: Executes the provided Python code and returns the printed output, if any.
#   Input: code (str). Example: "print('Hello, World!')". Output: Success message with the printed output (str) or error message (str).
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

        combined_message = f"{user_input_content}. If the task is not yet complete, remember to not only retrive reference literature but also Review the toolset before selecting detection methods. If you have already done it, there's no need to reply this."

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
def get_all_reference_intentions(
    references_file_path: Annotated[str, "The path to the JSON file containing the references data."]
) -> list[dict]:
    """
    Retrieve all intentions from the references JSON file.

    Args:
        references_file_path (str): The path to the JSON file containing the references data, which is source_files/references.json

    Returns:
        list[dict]: A list of dictionaries where each dictionary contains 'id' and 'intention'.
                    Example:
                    [
                        {"id": 1, "intention": "Detect bias in cardiovascular disease dataset..."},
                        {"id": 2, "intention": "Quantify performance differences using N-Sigma..."}
                    ]
    """
    try:
        # Load the JSON file with UTF-8 encoding
        with open(references_file_path, 'r', encoding='utf-8') as file:
            references = json.load(file)
        
        # Retrieve all intentions
        intentions = [{"id": ref["id"], "intention": ref["intention"]} for ref in references]

        # Add note to the result
        note = "You need to select appropriate intentions for your task from these references and use their IDs to call the get_reference_method_by_id tool to obtain the method for each reference."
        
        # Return the combined string
        return f"{intentions}\n\n{note}"
        
    except Exception as e:
        return {
            "error": f"Failed to retrieve intentions from references. Error: {repr(e)}"
        }
    
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
                return f"{method}\n\nYou MUST generate executable code based on this method ASAP and call the execute_python_code function to execute it."
        
        return {"error": f"Method for reference ID {id_to_retrieve} not found."}

    except Exception as e:
        return {
            "error": f"Failed to retrieve method for reference ID {id_to_retrieve}. Error: {repr(e)}"
        }

@tool
def generate_bias_report_pdf(
    content_sections: Annotated[list[dict], "List of content sections, where each section can be either text or an image."],
    output_pdf_path: Annotated[str, "The path to save the generated PDF report."]
) -> str:
    """
    Generate a flexible bias detection report in PDF format, including both text and charts.

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
        pdf.cell(0, 10, 'Bias Detection Report', ln=True, align='C')
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
                        # Process as a level 2 header
                        header_text = line.replace('# ', '')  # Remove '## '
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
        return f"Successfully created and saved the PDF report at: {output_pdf_path}"

    except Exception as e:
        return f"Failed to create PDF report. Error: {repr(e)}"

@tool
def execute_python_code(
    code: Annotated[str, "The python code to execute to generate your chart."],
):
    """Use this to execute Python code with persistent namespace."""
    import sys
    import io

    # 在 `execute_python_code` 自己的 `__dict__` 里存储 namespace
    if "namespace" not in execute_python_code.__dict__:
        execute_python_code.__dict__["namespace"] = {}

    namespace = execute_python_code.__dict__["namespace"]

    # 捕获标准输出
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        # 在 `namespace` 里执行代码，保持 `import` 变量
        exec(code, namespace)
        result_str = sys.stdout.getvalue()
    except BaseException as e:
        result_str = f"Failed to execute. Error: {repr(e)}"
    finally:
        # 恢复标准输出
        sys.stdout = old_stdout

    return f"Execution result:\n{result_str}"

