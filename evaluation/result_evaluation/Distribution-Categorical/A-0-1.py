import sys
import pandas as pd
import numpy as np
import math

def main():
    if len(sys.argv) != 2:
        print("Usage: python A-0-1.py <csv_file_path>")
        sys.exit(1)
    csv_file_path = sys.argv[1]

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Check if there is at least one feature column
    if df.shape[1] < 1:
        print("Error: The CSV file must contain at least one feature column.")
        sys.exit(1)

    # Get the name of the feature column (assuming only one feature column)
    feature_name = df.columns[0]

    # Handle missing values
    df = df.dropna(subset=[feature_name])

    # Determine the feature type
    if pd.api.types.is_numeric_dtype(df[feature_name]):
        print("Error: This script is designed for categorical features.")
        sys.exit(1)

    # Calculate the frequency of each category
    feature_counts = df[feature_name].value_counts()
    total = len(df)

    # Compute Shannon entropy
    H = 0
    for count in feature_counts:
        probability = count / total
        H -= probability * math.log(probability, 2)

    # Number of categories
    k = df[feature_name].nunique()

    # Calculate the balance metric
    if k > 1:
        Balance = H / math.log(k, 2)
    else:
        Balance = 0  # If only one category exists, balance metric is 0

    # print(Balance)  
    # Determine bias level based on the balance metric
    if Balance >= 0.95:
        bias_level = 'Level 1'
    elif 0.80  <= Balance < 0.95:
        bias_level = 'Level 2'
    elif 0.65 <= Balance < 0.80:
        bias_level = 'Level 3'
    elif 0.50 <= Balance < 0.65:
        bias_level = 'Level 4'
    else:
        bias_level = 'Level 5'

    # Output the bias level
    print(bias_level)

if __name__ == "__main__":
    main()
