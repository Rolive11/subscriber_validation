# How-To Guide for Subscriber Validation Script (vs.py)

This guide provides step-by-step instructions for using the `vs.py` Python script, which processes subscriber CSV files according to the flowchart in the Subscriber Validation Repository. The script creates a directory, copies the input CSV, adds a new column (`OrigRowNum`) to track the original row order for traceability, and creates a cleaned version of the CSV with standardized column titles.

## Prerequisites

Before running the script, ensure the following are set up on your system:

### 1. Python Installation
- **Python Version**: Python 3.x (e.g., Python 3.8 or later is recommended).
- Verify Python is installed by running:
  ```bash
  python3 --version
  ```
- If Python is not installed, download and install it from [python.org](https://www.python.org/downloads/).

### 2. Required Python Libraries
The script requires the following libraries:
- **Standard Libraries** (included with Python):
  - `os`: For directory and file operations.
  - `shutil`: For copying files and managing directories.
  - `sys`: For handling command-line arguments.
- **External Library**:
  - `pandas`: For CSV file reading, manipulation, and writing.
- To check if `pandas` is installed, run:
  ```bash
  pip show pandas
  ```
- If `pandas` is not installed, install it using:
  ```bash
  pip install pandas
  ```
  or, for Python 3 specifically:
  ```bash
  pip3 install pandas
  ```

### 3. Optional: Virtual Environment
To avoid conflicts with other Python projects, consider using a virtual environment:
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
2. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
3. Install `pandas` in the virtual environment:
   ```bash
   pip install pandas
   ```

### 4. Input CSV File
- Prepare a CSV file (e.g., `subscribers.csv`) with the following structure:
  - **12 columns** with exact, case-insensitive headers (in any order):
    ```
    customer,lat,lon,address,city,state,zip,download,upload,voip_lines_quantity,business_customer,technology
    ```
  - The `customer` column may have missing values, but other columns may contain data.
  - The CSV may include additional columns, which will be ignored in the cleaned output.
- Ensure the CSV file is accessible and readable from the directory where you’ll run the script.

## Script Overview
The `vs.py` script performs the following tasks:
1. Creates a directory named after the provided `company_id`.
2. Copies the input CSV to the `company_id` directory as `original_subscribers.csv`.
3. Reads the CSV and inserts a new column, `OrigRowNum`, as the first column.
4. Populates `OrigRowNum` with sequential numbers (starting from 1 in row 2) for all data rows to enable traceability.
5. Saves the modified CSV as `original_subscribers_columnA_inserted.csv` in the `company_id` directory.
6. Validates that all required columns (`customer`, `lat`, `lon`, `address`, `city`, `state`, `zip`, `download`, `upload`, `voip_lines_quantity`, `business_customer`, `technology`) are present in the CSV, ignoring case.
7. Creates a new CSV, `original_subscribers_cleantitles.csv`, using `original_subscribers_columnA_inserted.csv`, with only the required columns in the specified order and standardized lowercase titles.
8. Saves `original_subscribers_cleantitles.csv` in the `company_id` directory.

The `OrigRowNum` column allows you to sort the file later to reconstruct the original row order, even after modifications. The `original_subscribers_cleantitles.csv` file ensures standardized, lowercase column titles for consistency in downstream processing.

## How to Run the Script

### Step 1: Save the Script
1. Save the `vs.py` script to a directory (e.g., `subscriber_validation/vs.py`). The script should contain the following code:
   ```python
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

       # Step 7: Validate required columns (case-insensitive)
       required_columns = [
           "customer", "lat", "lon", "address", "city", "state", "zip",
           "download", "upload", "voip_lines_quantity", "business_customer", "technology"
       ]
       input_columns = df_inserted.columns.str.lower().tolist()  # Convert input column names to lowercase for comparison
       missing_columns = [col for col in required_columns if col not in input_columns]

       if missing_columns:
           print(f"Error: The following required columns are missing: {', '.join(missing_columns)}")
           sys.exit(1)

       # Step 8: Create new CSV with cleaned column titles
       output_cleantitles_csv = os.path.join(company_id, "original_subscribers_cleantitles.csv")
       
       # Map original column names to standardized lowercase names
       column_mapping = {col: col.lower() for col in df_inserted.columns if col.lower() in required_columns}
       # Select and reorder columns to match required_columns order, including OrigRowNum
       cleaned_df = df_inserted[list(column_mapping.keys()) + ["OrigRowNum"]].rename(columns=column_mapping)
       cleaned_df = cleaned_df[["OrigRowNum"] + required_columns]  # Reorder with OrigRowNum first
       
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
   ```

### Step 2: Prepare Your Environment
1. Open a terminal or command prompt.
2. Navigate to the directory containing `vs.py`:
   ```bash
   cd path/to/subscriber_validation
   ```
3. Ensure your input CSV file is in an accessible location (e.g., same directory as `vs.py` or a specified path).

### Step 3: Run the Script
Run the script using the following command:
```bash
python3 vs.py "path/to/your_input.csv" "company_id"
```
- Replace `path/to/your_input.csv` with the path to your CSV file (e.g., `subscribers.csv`).
- Replace `company_id` with a unique identifier for the company (e.g., `acme_corp`). This will be the name of the output directory.
- Example:
  ```bash
  python3 vs.py "subscribers.csv" "acme_corp"
  ```

### Step 4: Verify Output
After running the script, check the following:
1. A directory named `company_id` (e.g., `acme_corp`) is created in the same directory as `vs.py`.
2. Inside `company_id`, three files are created:
   - `original_subscribers.csv`: A copy of the input CSV.
   - `original_subscribers_columnA_inserted.csv`: The input CSV with a new `OrigRowNum` column.
   - `original_subscribers_cleantitles.csv`: A CSV with standardized lowercase column titles in the specified order (`OrigRowNum`, `customer`, `lat`, `lon`, etc.), created from `original_subscribers_columnA_inserted.csv`.
3. Open `original_subscribers_cleantitles.csv` to verify:
   - The first column is `OrigRowNum` with the header in row 1.
   - Rows 2 and beyond have sequential numbers (1, 2, 3, ...) in the `OrigRowNum` column.
   - The next 12 columns are `customer`, `lat`, `lon`, `address`, `city`, `state`, `zip`, `download`, `upload`, `voip_lines_quantity`, `business_customer`, `technology` (all lowercase).
4. Open `original_subscribers_columnA_inserted.csv` to verify:
   - The first column is `OrigRowNum` with the header in row 1.
   - Rows 2 and beyond have sequential numbers (1, 2, 3, ...) in the `OrigRowNum` column.
   - The original columns (including any extra columns) follow, starting with `customer`.

## Expected Input and Output

### Input CSV Example
Suppose your input CSV (`subscribers.csv`) looks like this, with mixed case and extra columns:
```
CUSTOMER,LAT,LON,ADDRESS,CITY,STATE,ZIP,EXTRA_COL,DOWNLOAD,UPLOAD,VOIP_LINES_QUANTITY,BUSINESS_CUSTOMER,TECHNOLOGY,ANOTHER_COL
John Doe,40.7128,-74.0060,123 Main St,New York,NY,10001,Extra1,100,20,2,Yes,Fiber,Extra2
,34.0522,-118.2437,456 Oak Ave,Los Angeles,CA,90001,Extra3,50,10,1,No,DSL,Extra4
Jane Smith,41.8781,-87.6298,789 Pine Rd,Chicago,IL,60601,Extra5,200,50,0,Yes,Fiber,Extra6
```

### Output Directory Structure
After running:
```bash
python3 vs.py "subscribers.csv" "acme_corp"
```
The `acme_corp` directory will contain:
- `original_subscribers.csv`: Identical to the input CSV, including all columns (e.g., `EXTRA_COL`, `ANOTHER_COL`).
- `original_subscribers_columnA_inserted.csv`:
  ```
  OrigRowNum,CUSTOMER,LAT,LON,ADDRESS,CITY,STATE,ZIP,EXTRA_COL,DOWNLOAD,UPLOAD,VOIP_LINES_QUANTITY,BUSINESS_CUSTOMER,TECHNOLOGY,ANOTHER_COL
  1,John Doe,40.7128,-74.0060,123 Main St,New York,NY,10001,Extra1,100,20,2,Yes,Fiber,Extra2
  2,,34.0522,-118.2437,456 Oak Ave,Los Angeles,CA,90001,Extra3,50,10,1,No,DSL,Extra4
  3,Jane Smith,41.8781,-87.6298,789 Pine Rd,Chicago,IL,60601,Extra5,200,50,0,Yes,Fiber,Extra6
  ```
- `original_subscribers_cleantitles.csv`:
  ```
  OrigRowNum,customer,lat,lon,address,city,state,zip,download,upload,voip_lines_quantity,business_customer,technology
  1,John Doe,40.7128,-74.0060,123 Main St,New York,NY,10001,100,20,2,Yes,Fiber
  2,,34.0522,-118.2437,456 Oak Ave,Los Angeles,CA,90001,50,10,1,No,DSL
  3,Jane Smith,41.8781,-87.6298,789 Pine Rd,Chicago,IL,60601,200,50,0,Yes,Fiber
  ```

### Notes
- The `OrigRowNum` column ensures every row (including those with missing `customer` values) is numbered sequentially.
- The script overwrites the `company_id` directory if it exists, so any previous files in that directory will be deleted.
- The script validates that all required columns are present (case-insensitive). If any are missing, it exits with an error.
- The `original_subscribers_cleantitles.csv` file is created from `original_subscribers_columnA_inserted.csv`, ensuring the `OrigRowNum` column is included and all required columns have standardized lowercase titles in the specified order.
- Extra columns in the input CSV are preserved in `original_subscribers.csv` and `original_subscribers_columnA_inserted.csv` but excluded from `original_subscribers_cleantitles.csv`.

## Troubleshooting
- **Error: "No module named 'pandas'"**
  - Install `pandas` using `pip install pandas`.
- **Error: "Input file does not exist"**
  - Ensure the CSV file path is correct and accessible. Use quotes around the path if it contains spaces.
- **Error: "The following required columns are missing"**
  - Verify that all required columns (`customer`, `lat`, etc.) are present in the input CSV, regardless of case.
- **No output directory created**
  - Check if the script ran successfully. Ensure you have write permissions in the directory where `vs.py` is located.
- **Unexpected CSV output**
  - Verify the input CSV includes the required columns. If issues persist, check the CSV for formatting errors (e.g., missing headers, extra commas).

## Next Steps
- **Header Validation**: The script currently checks for case-insensitive headers. Future updates may enforce exact spelling and case for stricter validation.
- **Error Handling**: Additional error handling will be added for malformed CSVs, empty files, or invalid `company_id` values.
- **Sorting**: The `OrigRowNum` column can be used to sort modified CSVs back to their original order in future processing steps.

For questions or issues, refer to the repository’s README or contact the repository maintainer.