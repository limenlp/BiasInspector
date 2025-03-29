import sys
import pandas as pd
import numpy as np

def main():
    if len(sys.argv) != 2:
        print("Usage: python A-0-4.py <csv_file_path>")
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

    # print(f"Corrected Gini Index: {corrected_gini_index:.4f}")
    # print(f"Adjusted Gini Index (relative to max): {adjusted_gini:.4f}")

    # Determine bias level based on the adjusted Gini Index
    if adjusted_gini >= 0.95:
        bias_level = 'Level 1'
    elif 0.80 <= adjusted_gini < 0.95:
        bias_level = 'Level 2'
    elif 0.65 <= adjusted_gini < 0.80:
        bias_level = 'Level 3'
    elif 0.40 <= adjusted_gini < 0.65:
        bias_level = 'Level 4'
    else:
        bias_level = 'Level 5'

    # Output the bias level
    print(f"{bias_level}")

if __name__ == "__main__":
    main()
