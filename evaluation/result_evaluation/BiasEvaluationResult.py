import os
import sys
import pandas as pd
import argparse
import subprocess
import re

def parse_arguments():
    parser = argparse.ArgumentParser(description='Bias Evaluation Result')
    parser.add_argument('--csv_file_path', type=str, required=True, help='Path to the CSV file')
    parser.add_argument('--bias_type', type=str, choices=['distribution', 'correlation'], required=True, help='Type of bias to detect')
    parser.add_argument('--feature_names', type=str, nargs='+', required=True, help='Feature names to analyze (one for distribution, two for correlation)')
    args = parser.parse_args()
    return args

def extract_data(csv_file_path, feature_names, bias_type):
    # Read the CSV file and skip spaces after the delimiter
    df = pd.read_csv(csv_file_path, skipinitialspace=True)
    # Remove spaces from column names and convert to lowercase
    df.columns = df.columns.str.replace(' ', '').str.lower()
    # Remove spaces from feature names and convert to lowercase
    feature_names = [name.replace(' ', '').lower() for name in feature_names]
    if bias_type == 'distribution':
        if len(feature_names) != 1:
            print("For distribution bias type, please provide exactly one feature name.")
            sys.exit(1)
        feature = feature_names[0]
        if feature not in df.columns.str.replace(' ', '').str.lower():
            print(f"Feature '{feature}' not found in CSV file.")
            print("Available columns are:", df.columns.tolist())  # For debugging
            sys.exit(1)
        df_new = df[[col for col in df.columns if col.replace(' ', '').lower() == feature]]
    elif bias_type == 'correlation':
        if len(feature_names) != 2:
            print("For correlation bias type, please provide exactly two feature names.")
            sys.exit(1)
        features = []
        for feature in feature_names:
            if feature not in df.columns.str.replace(' ', '').str.lower():
                print(f"Feature '{feature}' not found in CSV file.")
                print("Available columns are:", df.columns.tolist())  # For debugging
                sys.exit(1)
            col_name = [col for col in df.columns if col.replace(' ', '').lower() == feature][0]
            features.append(col_name)
        df_new = df[features]
    else:
        print("Invalid bias type.")
        sys.exit(1)

    # Parse date columns and convert to numeric timestamps
    for col in df_new.columns:
        try:
            df_new[col] = pd.to_datetime(df_new[col])
            df_new[col] = df_new[col].astype('int64')  # Convert datetime to integer timestamp
        except (ValueError, TypeError):
            pass  # If conversion fails, leave the column as is

    # Create a new folder to store the extracted feature file
    new_folder = 'ExtractedFeatures'
    os.makedirs(new_folder, exist_ok=True)
    new_csv_file_path = os.path.join(new_folder, 'extracted_features.csv')
    df_new.to_csv(new_csv_file_path, index=False)
    return new_csv_file_path, df_new

def determine_data_types(df_new, feature_names):
    data_types = []
    for feature in df_new.columns:
        dtype = df_new[feature].dtype
        if pd.api.types.is_numeric_dtype(dtype):
            data_types.append('numerical')
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            data_types.append('numerical')  # Treat datetime as numerical
        else:
            data_types.append('categorical')
    return data_types

def select_folder(bias_type, data_types):
    folder = ''
    if bias_type == 'distribution':
        if data_types[0] == 'categorical':
            folder = 'Distribution-Categorical'
        elif data_types[0] == 'numerical':
            folder = 'Distribution-Numerical'
        else:
            print("Unknown data type for feature.")
            sys.exit(1)
    elif bias_type == 'correlation':
        if data_types == ['categorical', 'categorical']:
            folder = 'Correlation-Categorical_Categorical'
        elif ('categorical' in data_types) and ('numerical' in data_types):
            folder = 'Correlation-Categorical_Numerical'
        elif data_types == ['numerical', 'numerical']:
            folder = 'Correlation-Numerical_Numerical'
        else:
            print("Unknown data types for features.")
            sys.exit(1)
    else:
        print("Invalid bias type.")
        sys.exit(1)
    return folder

def run_scripts_and_collect_outputs(folder, new_csv_file_path):
    results = []
    script_folder_path = os.path.join(os.getcwd(), folder)
    if not os.path.exists(script_folder_path):
        print(f"Folder '{folder}' does not exist.")
        sys.exit(1)
    script_files = [f for f in os.listdir(script_folder_path) if f.endswith('.py')]
    if not script_files:
        print(f"No python scripts found in folder '{folder}'.")
        sys.exit(1)

    print(f"\nRunning bias detection scripts in folder '{folder}':\n")
    for script_file in script_files:
        script_path = os.path.join(script_folder_path, script_file)
        try:
            result = subprocess.check_output([sys.executable, script_path, new_csv_file_path], universal_newlines=True)
            result = result.strip()
            results.append((script_file, result))
        except subprocess.CalledProcessError as e:
            print(f"Error running script '{script_file}': {e}")
            sys.exit(1)

    print("{:<35} {:<20}".format("Tool", "Output"))
    print("-" * 55)

    for tool_name, output in results:
        print("{:<35} {:<20}".format(tool_name, output))
    return [output for tool_name, output in results]

def map_outputs_to_numbers(outputs):
    number_outputs = []
    for output in outputs:
        match = re.search(r'Level (\d+)', output)
        if match:
            number = int(match.group(1))
            if 1 <= number <= 5:
                number_outputs.append(number)
            else:
                print(f"Invalid bias level number '{number}' in output '{output}'.")
                sys.exit(1)
        else:
            print(f"Output '{output}' does not match expected format.")
            sys.exit(1)
    return number_outputs

def select_highest_bias(number_outputs):
    highest_bias = max(number_outputs)
    return highest_bias

def get_bias_label(highest_bias):
    if highest_bias == 1:
        return 'Level 1'
    elif highest_bias == 2:
        return 'Level 2'
    elif highest_bias == 3:
        return 'Level 3'
    elif highest_bias == 4:
        return 'Level 4'
    elif highest_bias == 5:
        return 'Level 5'
    else:
        return 'Unknown Bias Level'

def main():
    args = parse_arguments()
    new_csv_file_path, df_new = extract_data(args.csv_file_path, args.feature_names, args.bias_type)
    data_types = determine_data_types(df_new, args.feature_names)
    folder = select_folder(args.bias_type, data_types)

    outputs = run_scripts_and_collect_outputs(folder, new_csv_file_path)
    number_outputs = map_outputs_to_numbers(outputs)
    highest_bias = select_highest_bias(number_outputs)
    bias_label = get_bias_label(highest_bias)

    print("\n" + "=" * 60)
    print("{:^60}".format("Final Bias Evaluation Result"))
    print("=" * 60)
    print("{:<30}: {}".format("Highest Bias Level", bias_label))
    print("=" * 60 + "\n")

if __name__ == '__main__':
    main()
