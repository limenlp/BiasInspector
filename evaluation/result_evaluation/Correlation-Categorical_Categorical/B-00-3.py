import sys
import pandas as pd
import numpy as np

def main():
    if len(sys.argv) != 2:
        print("Usage: python B-00-3.py <csv_file_path>")
        sys.exit(1)
    csv_file_path = sys.argv[1]

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Ensure there are exactly two categorical features
    if df.shape[1] != 2:
        print("Error: The CSV file must contain exactly two categorical features.")
        sys.exit(1)

    # Get feature names
    feature_x, feature_y = df.columns

    # Check data types
    if not (pd.api.types.is_object_dtype(df[feature_x]) or pd.api.types.is_categorical_dtype(df[feature_x])):
        print(f"Error: '{feature_x}' must be a categorical feature.")
        sys.exit(1)
    if not (pd.api.types.is_object_dtype(df[feature_y]) or pd.api.types.is_categorical_dtype(df[feature_y])):
        print(f"Error: '{feature_y}' must be a categorical feature.")
        sys.exit(1)

    # Drop missing values
    df = df.dropna(subset=[feature_x, feature_y])

    # Total number of records
    N = len(df)

    # Calculate overall proportion (mean)
    overall_proportion = df[feature_y].value_counts(normalize=True).to_dict()

    # Initialize a list to store statistical parity values
    parity_values = []

    # Iterate through all categories of feature_x
    for x_category in df[feature_x].unique():
        group_df = df[df[feature_x] == x_category]
        N_g = len(group_df)

        # Calculate group-specific proportion for feature_y
        group_proportion = group_df[feature_y].value_counts(normalize=True).to_dict()

        # Compute Z-scores to capture significant differences
        for y_category in df[feature_y].unique():
            overall_mean = overall_proportion.get(y_category, 0)
            group_mean = group_proportion.get(y_category, 0)

            # Calculate Z-score: (group_mean - overall_mean) / stddev
            stddev = np.sqrt(np.mean((df[feature_y] == y_category).astype(float)) * (1 - np.mean((df[feature_y] == y_category).astype(float))) + 1e-6)
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

    # Determine bias level based on Z_value
    if max_Z_value <= 0.25:  # Adjusted Z-score thresholds for finer detection
        bias_level = 'Level 1'
    elif max_Z_value <= 0.50:
        bias_level = 'Level 2'
    elif max_Z_value <= 0.75:
        bias_level = 'Level 3'
    elif max_Z_value <= 1.00:
        bias_level = 'Level 4'
    else:
        bias_level = 'Level 5'

    # Output bias level
    # print(f"Max Z-value: {max_Z_value}")
    print(bias_level)

if __name__ == "__main__":
    main()
