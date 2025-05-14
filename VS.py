import pandas as pd
import os
import shutil
import sys

def validate_subscriber_file(input_csv, company_id):
    # Step 1: Create or overwrite the company_id directory
    if os.path.exists(company_id):
        shutil.rmtree(company_id)  # Delete existing directory and contents
    os.makedirs(company_id)  # Create new directory

    # Step 2: Copy input CSV to company_id as original_subscribers.csv
    output_csv = os.path.join(company_id, "original_subscribers.csv")
    shutil.copyfile(input_csv, output_csv)

    # Step 3: Read the input CSV
    df = pd.read_csv(output_csv)

    # Step 4: Insert OrigRowNum column to the left of column A
    # Create sequential numbers for all data rows (excluding header)
    active_subscribers = len(df)  # Total number of data rows
    df.insert(0, "OrigRowNum", range(1, active_subscribers + 1))

    # Step 5: Save the modified DataFrame to original_subscribers_columnA_inserted.csv
    output_inserted_csv = os.path.join(company_id, "original_subscribers_columnA_inserted.csv")
    df.to_csv(output_inserted_csv, index=False)

    # Step 6: Read the CSV with OrigRowNum for further processing
    df_inserted = pd.read_csv(output_inserted_csv)

    # Debugging: Print columns in df_inserted
    print(f"Columns in original_subscribers_columnA_inserted.csv: {df_inserted.columns.tolist()}")

    # Step 7: Validate required columns (case-insensitive, excluding OrigRowNum)
    required_columns = [
        "customer", "lat", "lon", "address", "city", "state", "zip",
        "download", "upload", "voip_lines_quantity", "business_customer", "technology"
    ]
    input_columns = df_inserted.columns.str.lower().tolist()  # Convert input column names to lowercase for comparison
    missing_columns = [col for col in required_columns if col not in input_columns]

    if missing_columns:
        print(f"Error: The following required columns are missing: {', '.join(missing_columns)}")
        sys.exit(1)

    # Step 8: Create new CSV with cleaned column titles, including OrigRowNum
    output_cleantitles_csv = os.path.join(company_id, "original_subscribers_cleantitles.csv")
    
    # Define output columns including OrigRowNum
    output_columns = ["OrigRowNum"] + required_columns
    
    # Map original column names to standardized lowercase names
    column_mapping = {col: col.lower() if col.lower() in required_columns else col 
                     for col in df_inserted.columns 
                     if col.lower() in required_columns or col.lower() == "origrownum"}
    
    # Debugging: Print column_mapping
    print(f"Column mapping: {column_mapping}")

    # Select and reorder columns to match output_columns order
    try:
        cleaned_df = df_inserted[list(column_mapping.keys())].rename(columns=column_mapping)[output_columns]
    except KeyError as e:
        print(f"KeyError: {e}. Available columns: {df_inserted.columns.tolist()}")
        sys.exit(1)
    
    # Save the cleaned DataFrame to original_subscribers_cleantitles.csv
    cleaned_df.to_csv(output_cleantitles_csv, index=False)

    print(f"Processing complete. Files saved in {company_id}/:")
    print(f"- original_subscribers.csv (original copy)")
    print(f"- original_subscribers_columnA_inserted.csv (with OrigRowNum)")
    print(f"- original_subscribers_cleantitles.csv (cleaned column titles with OrigRowNum)")

if __name__ == "__main__":
    # Check for correct command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 vs.py <input_csv> <company_id>")
        sys.exit(1)

    input_csv = sys.argv[1]
    company_id = sys.argv[2]

    # Basic check for input file existence
    if not os.path.isfile(input_csv):
        print(f"Error: Input file '{input_csv}' does not exist.")
        sys.exit(1)

    validate_subscriber_file(input_csv, company_id)