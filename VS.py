import pandas as pd
import os
import shutil
import sys

def validate_subscriber_file(input_csv, company_id):
    # Step 1: Create or overwrite the company_id directory
    if os.path.exists(company_id):
        shutil.rmtree(company_id)  # Delete existing directory and contents
    os.makedirs(company_id)  # Create new directory

    # Step 2: Copy input CSV to company_id with original filename
    original_filename = os.path.basename(input_csv)
    output_original_csv = os.path.join(company_id, original_filename)
    shutil.copyfile(input_csv, output_original_csv)

    # Step 3: Read the input CSV
    df = pd.read_csv(input_csv)

    # Step 4: Insert OrigRowNum column
    df.insert(0, "OrigRowNum", range(1, len(df) + 1))

    # Step 5: Debugging - Print columns
    print(f"Columns in DataFrame: {df.columns.tolist()}")

    # Step 6: Validate required columns (case-insensitive)
    required_columns = [
        "customer", "lat", "lon", "address", "city", "state", "zip",
        "download", "upload", "voip_lines_quantity", "business_customer", "technology"
    ]
    input_columns = df.columns.str.lower().tolist()
    missing_columns = [col for col in required_columns if col not in input_columns]
    if missing_columns:
        print(f"Error: The following required columns are missing: {', '.join(missing_columns)}")
        sys.exit(1)

    # Step 7: Create cleaned DataFrame with standardized column titles
    output_columns = ["OrigRowNum"] + required_columns
    column_mapping = {col: col.lower() for col in df.columns 
                     if col.lower() in required_columns or col.lower() == "origrownum"}

    # Debugging - Print column mapping
    print(f"Column mapping: {column_mapping}")

    # Select and reorder columns
    try:
        cleaned_df = df[list(column_mapping.keys())].rename(columns=column_mapping)[output_columns]
    except KeyError as e:
        print(f"KeyError: {e}. Available columns: {df.columns.tolist()}")
        sys.exit(1)

    # Step 8: Save the cleaned DataFrame
    output_cleantitles_csv = os.path.join(company_id, "original_subscribers_cleantitles.csv")
    cleaned_df.to_csv(output_cleantitles_csv, index=False)

    print(f"Processing complete. Files saved in {company_id}/:")
    print(f"- {original_filename} (original copy)")
    print(f"- original_subscribers_cleantitles.csv (cleaned column titles with OrigRowNum)")

if __name__ == "__main__":
    # Check for correct command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 vs.py <input_csv> <company_id>")
        sys.exit(1)

    input_csv = sys.argv[1]
    company_id = sys.argv[2]

    # Check for input file existence
    if not os.path.isfile(input_csv):
        print(f"Error: Input file '{input_csv}' does not exist.")
        sys.exit(1)

    validate_subscriber_file(input_csv, company_id)