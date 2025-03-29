import sys
import pandas as pd
import numpy as np

# Calculate the max/min ratio of categories using relative frequency
def calculate_max_min_ratio(series):
    counts = series.value_counts(normalize=True)  # Use relative frequency
    max_ratio = counts.max()
    min_ratio = counts.min()
    # If the minimum category ratio is close to 0, treat it as a sign of extreme bias
    if min_ratio == 0:
        return float('inf')
    return max_ratio / min_ratio

def main():
    if len(sys.argv) != 2:
        print("Usage: python A-0-2.py <csv_file_path>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Automatically detect categorical features (non-numeric features)
    categorical_features = [col for col in df.columns if not pd.api.types.is_numeric_dtype(df[col])]

    if not categorical_features:
        print("Error: No categorical features found in the dataset.")
        sys.exit(1)

    # Evaluate each categorical feature
    for feature_column in categorical_features:
        # Remove missing values
        df_feature = df.dropna(subset=[feature_column])

        # Calculate the max/min ratio of the categories
        max_min_ratio = calculate_max_min_ratio(df_feature[feature_column])

        # Output max/min ratio
        # print(f"Max/Min Ratio of {feature_column}: {max_min_ratio}")

        # Bias level judgment based on the max/min ratio
        if max_min_ratio > 100:
            bias_level = 'Level 5'
        elif max_min_ratio > 10:
            bias_level = 'Level 4'
        elif max_min_ratio > 5:
            bias_level = 'Level 3'
        elif max_min_ratio > 2:
            bias_level = 'Level 2'
        else:
            bias_level = 'Level 1'

        # Output bias level
        print(f"{bias_level}")

if __name__ == "__main__":
    main()
