import sys
import pandas as pd
import numpy as np
from scipy import stats

# Function to calculate Average Direct Effect (ADE)
def calculate_ADE(group1, group2):
    # Average Direct Effect (ADE): Difference in means between two groups
    mu_group1 = np.mean(group1)
    mu_group2 = np.mean(group2)
    ADE = mu_group1 - mu_group2
    return ADE

# Function to calculate Average Indirect Effect (AIE)
def calculate_AIE(group1, group2):
    # Average Indirect Effect (AIE): Based on the variance within groups
    var_group1 = np.var(group1, ddof=1)
    var_group2 = np.var(group2, ddof=1)
    AIE = var_group2 - var_group1  # Indirect effect is defined as the difference in variances
    return AIE

# Function to calculate Path-Specific Effect (PSE)
def calculate_PSE(ADE, AIE):
    # Path-Specific Effect (PSE): Combine ADE and AIE
    PSE = ADE + np.abs(AIE)  # Use absolute AIE to ensure magnitude captures indirect effect
    return PSE

def main():
    if len(sys.argv) != 2:
        print("Usage: python B-01-5.py <csv_file_path>")
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

    # Step 2: Calculate ADE (Average Direct Effect)
    ADE = calculate_ADE(group1, group2)

    # Step 3: Calculate AIE (Average Indirect Effect)
    AIE = calculate_AIE(group1, group2)

    # Step 4: Calculate Path-Specific Effect (PSE)
    PSE = calculate_PSE(ADE, AIE)

    # Determine bias level based on PSE
    if PSE < 3:
        bias_level = 'Level 1'
    elif PSE < 4.5:
        bias_level = 'Level 2'
    elif PSE < 6:
        bias_level = 'Level 3'
    elif PSE < 7.5:
        bias_level = 'Level 4'
    else:
        bias_level = 'Level 5'

    # Output the bias level
    print(f"{bias_level}")

if __name__ == "__main__":
    main()
