# How-To Guide for Subscriber Validation Script (vs.py)

This guide provides step-by-step instructions for using the `vs.py` Python script, which processes subscriber CSV files according to the flowchart in the Subscriber Validation Repository. The script creates a directory, copies the input CSV, and adds a new column (`OrigRowNum`) to track the original row order for traceability.

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
  - **12 columns** with exact, case-sensitive headers (in order):
    ```
    customer,lat,lon,address,city,state,zip,download,upload,voip_lines_quantity,business_customer,technology
    ```
  - The `customer` column may have missing values, but other columns may contain data.
- Ensure the CSV file is accessible and readable from the directory where you’ll run the script.

## Script Overview
The `vs.py` script performs the following tasks:
1. Creates a directory named after the provided `company_id`.
2. Copies the input CSV to the `company_id` directory as `original_subscribers.csv`.
3. Reads the CSV and inserts a new column, `OrigRowNum`, as the first column.
4. Populates `OrigRowNum` with sequential numbers (starting from 1 in row 2) for all data rows to enable traceability.
5. Saves the modified CSV as `original_subscribers_columnA_inserted.csv` in the `company_id` directory.

The `OrigRowNum` column allows you to sort the file later to reconstruct the original row order, even after modifications.

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
2. Inside `company_id`, two files are created:
   - `original_subscribers.csv`: A copy of the input CSV.
   - `original_subscribers_columnA_inserted.csv`: The modified CSV with a new `OrigRowNum` column.
3. Open `original_subscribers_columnA_inserted.csv` to verify:
   - The first column is `OrigRowNum` with the header in row 1.
   - Rows 2 and beyond have sequential numbers (1, 2, 3, ...) in the `OrigRowNum` column.
   - The original 12 columns follow, starting with `customer`.

## Expected Input and Output

### Input CSV Example
Suppose your input CSV (`subscribers.csv`) looks like this:
```
customer,lat,lon,address,city,state,zip,download,upload,voip_lines_quantity,business_customer,technology
John Doe,40.7128,-74.0060,123 Main St,New York,NY,10001,100,20,2,Yes,Fiber
,34.0522,-118.2437,456 Oak Ave,Los Angeles,CA,90001,50,10,1,No,DSL
Jane Smith,41.8781,-87.6298,789 Pine Rd,Chicago,IL,60601,200,50,0,Yes,Fiber
```

### Output Directory Structure
After running:
```bash
python3 vs.py "subscribers.csv" "acme_corp"
```
The `acme_corp` directory will contain:
- `original_subscribers.csv`: Identical to the input CSV.
- `original_subscribers_columnA_inserted.csv`, which looks like:
  ```
  OrigRowNum,customer,lat,lon,address,city,state,zip,download,upload,voip_lines_quantity,business_customer,technology
  1,John Doe,40.7128,-74.0060,123 Main St,New York,NY,10001,100,20,2,Yes,Fiber
  2,,34.0522,-118.2437,456 Oak Ave,Los Angeles,CA,90001,50,10,1,No,DSL
  3,Jane Smith,41.8781,-87.6298,789 Pine Rd,Chicago,IL,60601,200,50,0,Yes,Fiber
  ```

### Notes
- The `OrigRowNum` column ensures every row (including those with missing `customer` values) is numbered sequentially.
- The script overwrites the `company_id` directory if it exists, so any previous files in that directory will be deleted.
- The script does not yet validate the CSV headers (e.g., for case sensitivity or correct spelling). Future updates will include this error handling.

## Troubleshooting
- **Error: "No module named 'pandas'"**
  - Install `pandas` using `pip install pandas`.
- **Error: "Input file does not exist"**
  - Ensure the CSV file path is correct and accessible. Use quotes around the path if it contains spaces.
- **No output directory created**
  - Check if the script ran successfully. Ensure you have write permissions in the directory where `vs.py` is located.
- **Unexpected CSV output**
  - Verify the input CSV has the expected 12 columns. If issues persist, check the CSV for formatting errors (e.g., missing headers, extra commas).

## Next Steps
- **Header Validation**: Future updates will include checks for case-sensitive, correctly spelled headers (`customer`, `lat`, etc.).
- **Error Handling**: Additional error handling will be added for malformed CSVs, empty files, or invalid `company_id` values.
- **Sorting**: The `OrigRowNum` column can be used to sort modified CSVs back to their original order in future processing steps.

For questions or issues, refer to the repository’s README or contact the repository maintainer.