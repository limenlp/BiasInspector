import sys
import pandas as pd
import numpy as np

def quantile_deviation(data):
    Q1 = np.percentile(data, 25)
    Q2 = np.percentile(data, 50)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1  # Interquartile Range
    return (Q3 - Q2) / IQR

def main():
    if len(sys.argv) != 2:
        print("Usage: python A-1-5.py <csv_file_path>")
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

    # Calculate quantile deviation
    q_dev = quantile_deviation(df[feature_name])

    # print(f"Quantile Deviation: {q_dev:.5f}")

    # Bias level determination based on quantile deviation (adjusted thresholds for higher sensitivity)
    if abs(q_dev) < 0.50:
        bias_level = 'Level 1'
    elif 0.50 <= abs(q_dev) < 0.56:
        bias_level = 'Level 2'
    elif 0.56 <= abs(q_dev) < 0.57:
        bias_level = 'Level 3'
    elif 0.57 <= abs(q_dev) < 0.58:
        bias_level = 'Level 4'
    else:
        bias_level = 'Level 5'

    # Output the bias level
    print(f"{bias_level}")

if __name__ == "__main__":
    main()
