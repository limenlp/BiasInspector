# B-00-1.py

import sys
import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np

def determine_bias_level(cramer_v):
    """
    Determine the bias level based on Cramér's V.
    """
    if cramer_v < 0.1:
        return 'Level 1'
    elif 0.1 <= cramer_v < 0.3:
        return 'Level 2'
    elif 0.3 <= cramer_v < 0.5:
        return 'Level 3'
    elif 0.5 <= cramer_v < 0.7:
        return 'Level 4'
    else:
        return 'Level 5'

def main():
    if len(sys.argv) != 2:
        print("Usage: python B-00-3.py <csv_file_path>")
        sys.exit(1)
    csv_file_path = sys.argv[1]

    # Read the CSV file
    try:
        df = pd.read_csv(csv_file_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    # Ensure there are exactly two categorical features
    if df.shape[1] != 2:
        print("Error: The CSV file must contain exactly two categorical features.")
        sys.exit(1)

    # Get feature names
    feature_a, feature_b = df.columns

    # Check data types
    if not (pd.api.types.is_object_dtype(df[feature_a]) or pd.api.types.is_categorical_dtype(df[feature_a])):
        print(f"Error: '{feature_a}' must be a categorical feature.")
        sys.exit(1)
    if not (pd.api.types.is_object_dtype(df[feature_b]) or pd.api.types.is_categorical_dtype(df[feature_b])):
        print(f"Error: '{feature_b}' must be a categorical feature.")
        sys.exit(1)

    # Drop missing values
    df = df.dropna(subset=[feature_a, feature_b])

    # Create contingency table
    contingency_table = pd.crosstab(df[feature_a], df[feature_b])

    # Check if the contingency table has sufficient data
    if contingency_table.size == 0:
        print("Error: Contingency table is empty. Check your data.")
        sys.exit(1)

    # Perform chi-square test
    try:
        chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)
    except Exception as e:
        print(f"Error performing chi-square test: {e}")
        sys.exit(1)

    # Calculate Cramér's V
    n = contingency_table.sum().sum()
    if n == 0:
        cramer_v = 0
    else:
        min_dim = min(contingency_table.shape) - 1
        if min_dim == 0:
            cramer_v = 0
        else:
            cramer_v = np.sqrt((chi2_stat / n) / min_dim)


    # Determine bias level
    bias_level = determine_bias_level(cramer_v)

    # Output bias level
    print(bias_level)

if __name__ == "__main__":
    main()
