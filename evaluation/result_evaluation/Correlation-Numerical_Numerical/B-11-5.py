import sys
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import rbf_kernel

def standardize_features(x, y):
    """Standardize features by subtracting their means and dividing by standard deviation."""
    x_standardized = (x - np.mean(x)) / np.std(x)
    y_standardized = (y - np.mean(y)) / np.std(y)
    return x_standardized, y_standardized

def compute_hsic(x, y, sigma=1.0):
    """Compute the Hilbert-Schmidt Independence Criterion (HSIC) using RBF kernels with sample size normalization."""
    # Compute RBF kernel matrices for x and y
    Kx = rbf_kernel(x.reshape(-1, 1), gamma=1/(2*sigma**2))
    Ky = rbf_kernel(y.reshape(-1, 1), gamma=1/(2*sigma**2))

    # Centering matrix
    n = Kx.shape[0]
    H = np.eye(n) - np.ones((n, n)) / n

    # Center the kernel matrices
    Kx_centered = H @ Kx @ H
    Ky_centered = H @ Ky @ H

    # Compute the HSIC value
    hsic_value = np.trace(Kx_centered @ Ky_centered)

    # Normalize by sample size to reduce the impact of sample size
    hsic_value /= (n - 1) ** 2  # Only normalize by sample size, no Frobenius norm

    return hsic_value

def determine_bias_level(hsic):
    """Determine bias level based on HSIC value."""
    if hsic < 0.001:
        return 'Level 1'
    elif  hsic < 0.01:
        return 'Level 2'
    elif hsic < 0.02:
        return 'Level 3'
    elif hsic < 0.03:
        return 'Level 4'
    else:
        return 'Level 5'

def main():
    if len(sys.argv) != 2:
        print("Usage: python B-11-5.py <csv_file_path>")
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

    # Standardize features
    x_standardized, y_standardized = standardize_features(x, y)

    # Compute HSIC using RBF kernel with sample size normalization
    hsic_value = compute_hsic(x_standardized, y_standardized)

    # Determine bias level based on HSIC
    bias_level = determine_bias_level(hsic_value)

    # Output HSIC value and bias level
    print(f"HSIC Value: {hsic_value}")
    print(f"Bias Level: {bias_level}")

if __name__ == "__main__":
    main()
