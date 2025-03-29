import sys
import pandas as pd
import numpy as np

def main():
    if len(sys.argv) != 2:
        print("Usage: python A-1-3.py <csv_file_path>")
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

    # Calculate mean and standard deviation
    mean = df[feature_name].mean()
    std = df[feature_name].std()

    # Compute Z-scores
    z_scores = (df[feature_name] - mean) / std

    # Count how many Z-scores are outside the threshold (e.g., |Z| > 3)
    outliers = np.sum(np.abs(z_scores) > 3)
    total_points = len(df[feature_name])
    outlier_percentage = (outliers / total_points) * 100

    # print(f"Outlier Percentage (|Z| > 3): {outlier_percentage:.2f}%")

    # Bias level determination based on outlier percentage
    if outlier_percentage < 0.5:
        bias_level = 'Level 1'
    elif 0.5 <= outlier_percentage < 0.75:
        bias_level = 'Level 2'
    elif 0.75 <= outlier_percentage < 0.90:
        bias_level = 'Level 3'
    elif 0.90 <= outlier_percentage < 3:
        bias_level = 'Level 4'
    else:
        bias_level = 'Level 5'

    # Output the bias level
    print(f"{bias_level}")

if __name__ == "__main__":
    main()
