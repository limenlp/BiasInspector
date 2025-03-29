# B-11-1.py

import sys
import pandas as pd
from scipy.stats import pearsonr

def main():
    if len(sys.argv) != 2:
        print("Usage: python B-11-1.py <csv_file_path>")
        sys.exit(1)
    csv_file_path = sys.argv[1]

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Ensure there are exactly two numerical features
    numerical_features = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numerical_features) != 2:
        print("Error: The CSV file must contain exactly two numerical features.")
        sys.exit(1)

    # Get feature names
    feature_x, feature_y = numerical_features

    # Drop missing values
    df = df.dropna(subset=[feature_x, feature_y])

    # Extract numerical data
    x = df[feature_x]
    y = df[feature_y]

    # Calculate Pearson correlation coefficient and p-value
    r_value, p_value = pearsonr(x, y)
    abs_r = abs(r_value)

    # print("Pearson Correlation Coefficient: ", abs_r)

    # Determine bias level based on correlation coefficient
    if abs_r < 0.2:
        bias_level = 'Level 1'
    elif 0.2 <= abs_r < 0.4:
        bias_level = 'Level 2'
    elif 0.4 <= abs_r < 0.6:
        bias_level = 'Level 3'
    elif 0.6 <= abs_r < 0.8:
        bias_level = 'Level 4'
    elif abs_r >= 0.8:
        bias_level = 'Level 5'
    else:
        bias_level = 'Level 5'

    # Output bias level
    print(bias_level)

if __name__ == "__main__":
    main()
