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

    # Step 4: Create new CSV with inserted column
    output_inserted_csv = os.path.join(company_id, "original_subscribers_columnA_inserted.csv")

    # Step 5: Insert OrigRowNum column to the left of column A
    # Create sequential numbers for all data rows (excluding header)
    active_subscribers = len(df)  # Total number of data rows
    df.insert(0, "OrigRowNum", range(1, active_subscribers + 1))

    # Step 6: Save the modified DataFrame to original_subscribers_columnA_inserted.csv
    df.to_csv(output_inserted_csv, index=False)

    print(f"Processing complete. Files saved in {company_id}/")

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