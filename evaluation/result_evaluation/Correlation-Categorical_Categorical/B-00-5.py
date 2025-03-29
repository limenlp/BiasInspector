import sys
import pandas as pd
import numpy as np

def total_variation_distance(p1, p2):
    """
    Calculate the Total Variation Distance between two distributions.
    :param p1: Distribution 1 (array of probabilities).
    :param p2: Distribution 2 (array of probabilities).
    :return: Total Variation Distance.
    """
    return 0.5 * np.sum(np.abs(p1 - p2))

def main():
    if len(sys.argv) != 2:
        print("Usage: python B-00-5.py <csv_file_path>")
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

    # Initialize a list to store Total Variation Distances
    tv_distances = []

    # Overall distribution of feature_y
    overall_distribution = df[feature_y].value_counts(normalize=True).sort_index()

    # Iterate through each category in feature_x
    for x_category in df[feature_x].unique():
        # Subset for this category
        subset = df[df[feature_x] == x_category]

        # Distribution of feature_y for this subset
        subset_distribution = subset[feature_y].value_counts(normalize=True).sort_index()

        # Align distributions for consistent comparison
        subset_distribution = subset_distribution.reindex(overall_distribution.index, fill_value=0)

        # Calculate Total Variation Distance between the overall distribution and the group distribution
        tv_distance = total_variation_distance(overall_distribution.values, subset_distribution.values)
        tv_distances.append({
            'X': x_category,
            'Total Variation Distance': tv_distance
        })

    # Find the maximum Total Variation Distance
    max_tv_distance = max([item['Total Variation Distance'] for item in tv_distances])

    # Determine bias level based on Total Variation Distance
    if max_tv_distance <= 0.1:
        bias_level = 'Level 1'
    elif max_tv_distance <= 0.2:
        bias_level = 'Level 2'
    elif max_tv_distance <= 0.3:
        bias_level = 'Level 3'
    elif max_tv_distance <= 0.4:
        bias_level = 'Level 4'
    else:
        bias_level = 'Level 5'

    # Output bias level
    print(bias_level)

if __name__ == "__main__":
    main()
