import sys
import pandas as pd
import numpy as np

def cohen_d_mad(data):
    """
    Calculate Cohen's d using Median Absolute Deviation (MAD) instead of standard deviation
    to reduce the sensitivity to sample size.
    """
    # Median and MAD calculation
    median_value = np.median(data)
    mad = np.median(np.abs(data - median_value))  # Median absolute deviation

    # If MAD is 0, add a small constant to avoid division by zero
    if mad == 0:
        mad = 1e-6  # Small constant

    mean_diff = np.mean(data) - median_value
    return mean_diff / mad

def main():
    if len(sys.argv) != 2:
        print("Usage: python A-1-4.py <csv_file_path>")
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

    # Ensure the feature is numeric
    if not pd.api.types.is_numeric_dtype(df[feature_name]):
        print("Error: This script is designed for numeric features.")
        sys.exit(1)

    # Calculate modified Cohen's d (using MAD instead of standard deviation)
    cohen_d_value = cohen_d_mad(df[feature_name])

    # print(f"{cohen_d_value:.5f}")

    # Determine bias based on modified Cohen's d
    if abs(cohen_d_value) < 0.1:
        bias_level = 'Level 1'
    elif 0.1 <= abs(cohen_d_value) < 0.2:
        bias_level = 'Level 2'
    elif 0.2 <= abs(cohen_d_value) < 0.3:
        bias_level = 'Level 3'
    elif 0.3 <= abs(cohen_d_value) < 0.4:
        bias_level = 'Level 4'
    else:
        bias_level = 'Level 5'

    # Output the bias level
    print(f"{bias_level}")

if __name__ == "__main__":
    main()
