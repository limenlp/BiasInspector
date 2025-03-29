import sys
import pandas as pd
import numpy as np

def calculate_mad(series):
    """Calculate Median Absolute Deviation (MAD)"""
    median = series.median()
    mad = np.median(np.abs(series - median))
    return mad

def main():
    if len(sys.argv) != 2:
        print("Usage: python B-01-3.py <csv_file_path>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Ensure the CSV file contains exactly two features
    if df.shape[1] != 2:
        print("Error: The CSV file must contain exactly two features (one categorical and one numerical).")
        sys.exit(1)

    # Get feature names
    feature1, feature2 = df.columns

    # Identify which feature is categorical and which is numerical
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

    # Step 1: Calculate the mean and std for the numerical feature by category
    grouped_stats = df.groupby(categorical_feature)[numerical_feature].agg(['mean', 'std']).reset_index()

    # Step 2: Calculate overall mean for the numerical feature
    overall_mean = df[numerical_feature].mean()

    # Step 3: Calculate Standardized Difference (SD) using a robust standard deviation (MAD)
    robust_std = calculate_mad(df[numerical_feature])  # Manually calculating MAD

    grouped_stats['Standardized_Difference'] = (grouped_stats['mean'] - overall_mean) / robust_std

    # Step 4: Determine bias level based on standardized difference
    def bias_level(sd_value):
        # print(abs(sd_value))
        if abs(sd_value) < 0.1:
            return 'Level 1'
        elif abs(sd_value) < 0.3:
            return 'Level 2'
        elif abs(sd_value) < 0.5:
            return 'Level 3'
        elif abs(sd_value) < 0.7:
            return 'Level 4'
        else:
            return 'Level 5'

    # Get the bias level for the first category
    if len(grouped_stats) < 1:
        print("Error: No categories found.")
        sys.exit(1)
        
    first_category_sd = grouped_stats['Standardized_Difference'].iloc[0]
    bias_evaluation = bias_level(first_category_sd)

    # Output the bias level
    print(bias_evaluation)

if __name__ == "__main__":
    main()
