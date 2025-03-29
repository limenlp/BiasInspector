import sys
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.neighbors import KernelDensity

# Step 1: Approximate HGR using Pearson correlation coefficient
def calculate_pearson_correlation(x, y):
    # Step 2: Pearson correlation as an approximation for linear correlation
    pearson_corr, _ = pearsonr(x, y)
    return pearson_corr

# Step 4: Use Kernel Density Estimation to approximate joint and marginal distributions
def estimate_distribution(x, y):
    # Joint distribution using KDE with adjusted bandwidth
    xy = np.vstack([x, y]).T
    kde_joint = KernelDensity(kernel='gaussian', bandwidth=0.1).fit(xy)  # Adjusted bandwidth
    log_joint_density = kde_joint.score_samples(xy)
    joint_density = np.exp(log_joint_density)

    # Marginal distributions
    kde_x = KernelDensity(kernel='gaussian', bandwidth=1000).fit(x.reshape(-1, 1))  # Adjusted bandwidth
    kde_y = KernelDensity(kernel='gaussian', bandwidth=1000).fit(y.reshape(-1, 1))  # Adjusted bandwidth

    log_marginal_x_density = kde_x.score_samples(x.reshape(-1, 1))
    log_marginal_y_density = kde_y.score_samples(y.reshape(-1, 1))

    marginal_x_density = np.exp(log_marginal_x_density)
    marginal_y_density = np.exp(log_marginal_y_density)

    return joint_density, marginal_x_density, marginal_y_density

# Step 5: Calculate normalized χ² divergence to assess bias strength
def calculate_chi_square_divergence(joint_density, marginal_x_density, marginal_y_density):
    # Calculate chi-square divergence
    chi_square_divergence = np.sum((joint_density - marginal_x_density * marginal_y_density) ** 2)

    # Add a small constant to avoid zero division
    normalization_factor = np.sum(joint_density) + 1e-10

    # Normalize chi-square divergence by joint density sum to make it independent of sample size
    normalized_chi_square = chi_square_divergence / normalization_factor

    return normalized_chi_square

# Step 6: Determine bias strength based on χ² divergence
def determine_bias_level(chi_square_value):
    # print(f"Normalized χ² Divergence: {chi_square_value}")
    if chi_square_value < 0.1:
        return 'Level 1'
    elif 0.1 <= chi_square_value < 0.3:
        return 'Level 2'
    elif 0.3 <= chi_square_value < 0.5:
        return 'Level 3'
    elif 0.5 <= chi_square_value < 0.7:
        return 'Level 4'
    else:
        return 'Level 5'

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

    # Step 1 & 2: Calculate Pearson correlation (approximate HGR)
    pearson_corr = calculate_pearson_correlation(x, y)
    # print(f"Pearson Correlation (HGR Approximation): {pearson_corr}")

    # Step 3 & 4: Estimate joint and marginal distributions using KDE
    joint_density, marginal_x_density, marginal_y_density = estimate_distribution(x, y)

    # Step 5: Calculate χ² divergence and normalize
    chi_square_value = calculate_chi_square_divergence(joint_density, marginal_x_density, marginal_y_density)

    # Step 6: Determine bias level based on normalized χ² divergence
    bias_level = determine_bias_level(chi_square_value)

    # Output bias level
    print(bias_level)

if __name__ == "__main__":
    main()
