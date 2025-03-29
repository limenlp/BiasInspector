import sys
import pandas as pd
import numpy as np

def main():
    if len(sys.argv) != 2:
        print("Usage: python B-01-1.py <csv_file_path>")
        sys.exit(1)
    csv_file_path = sys.argv[1]

    # Read the CSV file
    try:
        df = pd.read_csv(csv_file_path)
    except Exception as e:
        print("Level 1")  # Default to 'No Bias' on read error
        sys.exit(1)

    # Identify categorical and numerical columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns

    if len(categorical_cols) != 1 or len(numerical_cols) != 1:
        print("Level 1")  # Default to 'No Bias' if column requirements are not met
        sys.exit(1)

    feature_cat = categorical_cols[0]
    feature_num = numerical_cols[0]

    # Drop rows with missing values in the relevant columns
    df = df.dropna(subset=[feature_cat, feature_num])

    if df.empty:
        print("Level 1")  # Default to 'No Bias' if dataframe is empty after dropping NaNs
        sys.exit(1)

    # Standardize the numerical feature to remove dependency on sample size
    df[feature_num] = (df[feature_num] - df[feature_num].mean()) / df[feature_num].std(ddof=0)

    # Get unique categories
    categories = df[feature_cat].unique()

    # Calculate N values for each category
    N_values = []
    for category in categories:
        group = df[df[feature_cat] == category][feature_num]
        group_mean = group.mean()  # Since data is standardized, this is effectively the z-score
        N_values.append(group_mean)  # Already standardized, so no need for extra normalization

    # Find the maximum absolute N value
    max_abs_N = max(abs(N) for N in N_values)

    # print(max_abs_N)

    # Adjusted bias level thresholds for higher sensitivity
    if max_abs_N < 0.1:
        bias_level = 'Level 1'
    elif max_abs_N < 0.2:
        bias_level = 'Level 2'
    elif max_abs_N < 0.3:
        bias_level = 'Level 3'
    elif max_abs_N < 0.4:
        bias_level = 'Level 4'
    else:
        bias_level = 'Level 5'

    # Output the bias level
    print(bias_level)

if __name__ == "__main__":
    main()
