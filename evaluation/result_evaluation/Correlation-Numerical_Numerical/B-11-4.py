import sys
import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance
from sklearn.preprocessing import StandardScaler

# Step 1: Standardize numerical features (to make them comparable)
def standardize_features(x, y):
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x.reshape(-1, 1)).flatten()
    y_scaled = scaler.fit_transform(y.reshape(-1, 1)).flatten()
    return x_scaled, y_scaled

# Step 2: Calculate Wasserstein-2 distance (no normalization by variance or sample size)
def calculate_wasserstein_distance(x, y):
    # Directly calculate Wasserstein-2 distance without normalization
    w_distance = wasserstein_distance(x, y)
    return w_distance

# Step 5: Determine bias level based on fixed Wasserstein-2 distance thresholds (not dependent on sample size)
def determine_bias_level(wasserstein_value):
    # Fixed thresholds based on Wasserstein-2 distance only
    if wasserstein_value < 0.0001:
        return 'Level 5'
    elif wasserstein_value < 0.001:
        return 'Level 4'
    elif wasserstein_value < 0.01:
        return 'Level 3'
    elif wasserstein_value < 0.02:
        return 'Level 2'
    else:
        return 'Level 1'

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file_path>")
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
    x = df[feature_x].values
    y = df[feature_y].values

    # Standardize the features
    x_scaled, y_scaled = standardize_features(x, y)

    # Step 2: Calculate Wasserstein-2 distance
    wasserstein_value = calculate_wasserstein_distance(x_scaled, y_scaled)
    # print(f"Wasserstein-2 Distance: {wasserstein_value}")

    # Step 5: Determine bias level based on fixed Wasserstein-2 distance thresholds
    bias_level = determine_bias_level(wasserstein_value)

    # Output bias level
    print(f"{bias_level}")

if __name__ == "__main__":
    main()
