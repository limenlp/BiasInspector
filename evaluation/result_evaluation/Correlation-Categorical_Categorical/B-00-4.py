import sys
import pandas as pd
import numpy as np

def main():
    if len(sys.argv) != 2:
        print("Usage: python B-00-4.py <csv_file_path>")
        sys.exit(1)
    csv_file_path = sys.argv[1]

    # Step 1: Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Ensure there are two categorical features
    if df.shape[1] != 2:
        print("Error: The CSV file must contain exactly two categorical features.")
        sys.exit(1)

    feature_x, feature_y = df.columns

    # Check if the features are categorical
    if not (pd.api.types.is_object_dtype(df[feature_x]) or pd.api.types.is_categorical_dtype(df[feature_x])):
        print(f"Error: '{feature_x}' must be a categorical feature.")
        sys.exit(1)
    if not (pd.api.types.is_object_dtype(df[feature_y]) or pd.api.types.is_categorical_dtype(df[feature_y])):
        print(f"Error: '{feature_y}' must be a categorical feature.")
        sys.exit(1)

    df = df.dropna(subset=[feature_x, feature_y])

    # Step 1: Set the weighted loss function for each categorical group
    overall_loss = df[feature_y].value_counts(normalize=True).to_dict()

    # Initialize a list to store results
    results = []

    # Step 2: Define the overall loss function for each group
    for x_category in df[feature_x].unique():
        group_df = df[df[feature_x] == x_category]
        group_loss = group_df[feature_y].value_counts(normalize=True).to_dict()

        # Step 3: Use a continuous Lipschitz function to represent the loss differences, f(l) = sum(sqrt(l_k))
        for y_category in df[feature_y].unique():
            overall_mean = overall_loss.get(y_category, 0)
            group_mean = group_loss.get(y_category, 0)

            # Step 4: Calculate the difference between the group loss and the overall mean loss Δ = (l_G - l) / σ
            stddev = np.sqrt(np.mean((df[feature_y] == y_category).astype(float)) * (1 - np.mean((df[feature_y] == y_category).astype(float))) + 1e-6)
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

    # print("max_delta:", max_delta)

    if max_delta <= 0.25:
        bias_level = 'Level 1'
    elif max_delta <= 0.50:
        bias_level = 'Level 2'
    elif max_delta <= 0.75:
        bias_level = 'Level 3'
    elif max_delta <= 1.0:
        bias_level = 'Level 4'
    else:
        bias_level = 'Level 5'

    # Step 6: Output the bias level
    print(bias_level)

if __name__ == "__main__":
    main()
