import sys
import pandas as pd
import dowhy
from dowhy import CausalModel
import warnings
import contextlib
import io

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def main():
    if len(sys.argv) != 2:
        print("Usage: python B-01-4.py <csv_file_path>")
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

    # Drop missing values
    df = df.dropna(subset=[numerical_feature, categorical_feature])

    # Convert categorical feature to a numerical encoding if necessary
    if not pd.api.types.is_numeric_dtype(df[categorical_feature]):
        df[categorical_feature] = pd.Categorical(df[categorical_feature]).codes

    # Step 1: Create a Causal Model using DoWhy
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        model = CausalModel(
            data=df,
            treatment=categorical_feature,
            outcome=numerical_feature,
            common_causes=[]  # No common causes provided in this case
        )

        # Step 2: Identify the causal effect
        identified_estimand = model.identify_effect()

        # Step 3: Estimate the causal effect using linear regression
        estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")

    # Step 4: Output the estimated effect
    ace_value = estimate.value
    # print(f"Estimated Causal Effect (ACE): {ace_value}")

    # Step 5: Determine bias level based on ACE
    if abs(ace_value) < 1:
        bias_level = 'Level 1'
    elif abs(ace_value) < 3:
        bias_level = 'Level 2'
    elif abs(ace_value) < 6:
        bias_level = 'Level 3'
    elif abs(ace_value) < 9:
        bias_level = 'Level 4'
    else:
        bias_level = 'Level 5'

    # Output the bias level
    print(f"{bias_level}")

if __name__ == "__main__":
    main()