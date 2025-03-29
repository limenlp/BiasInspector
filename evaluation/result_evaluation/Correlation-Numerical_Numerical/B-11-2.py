import sys
import pandas as pd
import numpy as np
from sklearn.metrics import normalized_mutual_info_score

def compute_normalized_mutual_information(x, y, bins=10):
    # Discretize x and y into bins
    x_binned = np.digitize(x, np.linspace(min(x), max(x), bins))
    y_binned = np.digitize(y, np.linspace(min(y), max(y), bins))

    # Calculate normalized mutual information
    nmi = normalized_mutual_info_score(x_binned, y_binned)
    
    # print("Normalized Mutual Information: ", nmi)
    return nmi

def determine_bias_level(nmi):
    # Modify the thresholds to make smaller NMI indicate more bias
    if nmi < 0.1:
        return 'Level 1'
    elif 0.1 <= nmi < 0.3:
        return 'Level 2'
    elif 0.3 <= nmi < 0.5:
        return 'Level 3'
    elif 0.5 <= nmi < 0.7:
        return 'Level 4'
    else:
        return 'Level 5'

def main():
    if len(sys.argv) != 2:
        print("Usage: python B-11-2.py <csv_file_path>")
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

    # Calculate normalized mutual information
    nmi = compute_normalized_mutual_information(x, y)

    # Determine bias level based on normalized mutual information
    bias_level = determine_bias_level(nmi)

    # Output bias level
    print(bias_level)

if __name__ == "__main__":
    main()
