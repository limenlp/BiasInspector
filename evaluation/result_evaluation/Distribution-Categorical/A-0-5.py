import sys
import pandas as pd

def main():
    if len(sys.argv) != 2:
        print("Usage: python A-0-5.py <csv_file_path>")
        sys.exit(1)
    csv_file_path = sys.argv[1]

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Check if there is at least one feature column
    if df.shape[1] < 1:
        print("Error: The CSV file must contain at least one feature column.")
        sys.exit(1)

    # Get the name of the feature column (assuming only one feature column)
    feature_name = df.columns[0]

    # Handle missing values
    df = df.dropna(subset=[feature_name])

    # Calculate the frequency of each category
    feature_counts = df[feature_name].value_counts(normalize=True)

    # Calculate the expected frequency assuming uniform distribution
    expected_frequency = 1 / len(feature_counts)

    # Calculate the relative risks
    relative_risks = feature_counts / expected_frequency

    # Compute the ratio of max relative risk to min relative risk
    max_relative_risk = relative_risks.max()
    min_relative_risk = relative_risks.min()

    # Calculate normalized bias score (ratio of max to min relative risk)
    normalized_bias_score = max_relative_risk / min_relative_risk if min_relative_risk > 0 else max_relative_risk

    # Determine bias level based on the normalized bias score
    if normalized_bias_score >= 100.0:
        bias_level = 'Level 5'
    elif 10.0 <= normalized_bias_score < 100.0:
        bias_level = 'Level 4'
    elif 3.0 <= normalized_bias_score < 10.0:
        bias_level = 'Level 3'
    elif 1.1 <= normalized_bias_score < 3.0:
        bias_level = 'Level 2'
    else:
        bias_level = 'Level 1'

    # Output the normalized bias score and level
    # print(f"Normalized Bias Score: {normalized_bias_score:.4f}")
    print(f"{bias_level}")

if __name__ == "__main__":
    main()
