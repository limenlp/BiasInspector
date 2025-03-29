import sys
import pandas as pd
import numpy as np
from scipy import stats

def main():
    if len(sys.argv) != 2:
        print("Usage: python B-01-2.py <csv_file_path>")
        sys.exit(1)
    csv_file_path = sys.argv[1]

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Ensure there are exactly two features
    if df.shape[1] != 2:
        print("Error: The CSV file must contain exactly two features (one categorical and one numerical).")
        sys.exit(1)

    # Get feature names
    feature1, feature2 = df.columns

    # Determine which feature is categorical and which is numerical
    if pd.api.types.is_numeric_dtype(df[feature1]):
        numerical_feature = feature1
        categorical_feature = feature2
    elif pd.api.types.is_numeric_dtype(df[feature2]):
        numerical_feature = feature2
        categorical_feature = feature1
    else:
        print("Error: One feature must be numerical.")
        sys.exit(1)

    if not (pd.api.types.is_object_dtype(df[categorical_feature]) or pd.api.types.is_categorical_dtype(df[categorical_feature])):
        print(f"Error: '{categorical_feature}' must be a categorical feature.")
        sys.exit(1)

    # Drop missing values
    df = df.dropna(subset=[numerical_feature, categorical_feature])

    # Get unique categories
    categories = df[categorical_feature].unique()
    num_categories = len(categories)

    if num_categories != 2:
        print("Error: This script supports only two categories.")
        sys.exit(1)

    # Get data for each category
    group1 = df[df[categorical_feature] == categories[0]][numerical_feature]
    group2 = df[df[categorical_feature] == categories[1]][numerical_feature]

    # Perform t-test
    stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)

    # Calculate Cohen's d
    s1 = np.var(group1, ddof=1)
    s2 = np.var(group2, ddof=1)
    s_pooled = np.sqrt((s1 + s2) / 2)  # Adjust pooled standard deviation to remove sample size dependency
    if s_pooled == 0:
        effect_size = 0
    else:
        d = (np.mean(group1) - np.mean(group2)) / s_pooled
        effect_size = abs(d)

    # print(effect_size)

    # Determine bias level based on effect size
    if effect_size < 0.25:
        bias_level = 'Level 1'
    elif effect_size < 0.5:
        bias_level = 'Level 2'
    elif effect_size < 0.75:
        bias_level = 'Level 3'
    elif effect_size < 1.00:
        bias_level = 'Level 4'
    else:
        bias_level = 'Level 5'

    # Output the bias level
    print(bias_level)

if __name__ == "__main__":
    main()
