# Subscriber Validation Repository

This repository contains tools and documentation for validating subscriber CSV files.

## Flowchart for Step 1 Validation
```mermaid
graph TD
    A[Start: Input the Subscriber CSV File and Company ID] --> B[Create or Overwrite a Directory called 'ID' off of the main directory, where ID is the imported Company ID] --> C[Save the Original Subscribers file in the new directory] --> D[Add a new column A to the subscriber file, Titled 'Cust_ID'] --> E[Starting with Row 2, add a sequence of ascending numbers starting at 1 up the the last row of the file containing data] --> F[Save this file in the directory 'ID' and call it '1st_Modified_Sub_File.csv]
    B --> C{Check for Exact Sequence of 12 Columns: <br>customer, lat, long, address, city, state, zip, <br>download, upload, voip_lines_quantity, <br>business_customer, technology}
    C -->|Found| D[Step 1: True - Exact Sequence Present]
    C -->|Not Found| E[Step 1: False - Sequence Missing or Incorrect]
    D --> F[Proceed to Next Validation Step]
    E --> G[Handle Missing/Incorrect Columns]