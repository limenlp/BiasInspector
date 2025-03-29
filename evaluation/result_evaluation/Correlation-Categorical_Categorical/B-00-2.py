# B-00-2.py

import sys
import pandas as pd
import numpy as np

def main():
    if len(sys.argv) != 2:
        print("Usage: python B-00-2.py <csv_file_path>")
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

    # Get the categories of feature X and Y
    categories_x = df[feature_x].unique()
    categories_y = df[feature_y].unique()

    # Initialize the list to store elift values
    elift_values = []

    # Calculate conf(Y)
    conf_y = df[feature_y].value_counts(normalize=True).to_dict()

    # Iterate through all combinations of X and Y categories
    for x in categories_x:
        supp_x = len(df[df[feature_x] == x]) / N  # supp(X)
        for y in categories_y:
            supp_y = len(df[df[feature_y] == y]) / N  # supp(Y)
            supp_xy = len(df[(df[feature_x] == x) & (df[feature_y] == y)]) / N  # supp(X, Y)
            if supp_x == 0 or conf_y[y] == 0:
                continue
            conf_x_to_y = supp_xy / supp_x  # conf(X -> Y)
            elift = conf_x_to_y / conf_y[y]  # elift(X -> Y)

            # Store the results
            elift_values.append({
                'X': x,
                'Y': y,
                'support_X': supp_x,
                'support_Y': supp_y,
                'support_XY': supp_xy,
                'confidence_X_to_Y': conf_x_to_y,
                'conf_Y': conf_y[y],
                'elift': elift
            })
            

    # Find the maximum elift value
    max_elift = max([item['elift'] for item in elift_values])

    # Determine bias level
    if max_elift <= 1.25:
        bias_level = 'Level 1'
    elif max_elift <= 1.5:
        bias_level = 'Level 2'
    elif max_elift <= 2.0:  # Lowered this threshold
        bias_level = 'Level 3'
    elif max_elift <= 2.5:  # Adjusted this too
        bias_level = 'Level 4'
    else:
        bias_level = 'Level 5'

    # Output bias level
    print(bias_level)

if __name__ == "__main__":
    main()
