# Subscriber Validation Repository

This repository contains tools and documentation for validating subscriber CSV files.

## Flowchart for Step 1 Validation
```mermaid
graph TD
    A[Start: Using the Terminal from the main_directory, Input the 'original_subscriber.csv' File and 'company_id', using this command line: python3 vs.py 'original_subscriber.csv' 'company_id'] --> B[Create/Overwrite a directory called 'company_id' off of the main directory] 
    B --> C[Save the 'original_subscribers.csv file in the new directory called 'company_id'] 
    C --> D[Create a new csv file called 'original_subscribers_columnA_inserted.csv' and save it to the 'company_id' directory] 
    D --> E[Copy the contents of 'original_subscribers.csv to 'original_subscribers_columnA_inserted.csv']
    E --> F[Open 'original_subscribers_columnA_inserted.csv' and insert a column to the left of column A and save the file]
    F --> G[Open 'original_subscribers_columnA_inserted.csv' and count the number of rows between row 2 and the end of the file where data is included in column B, and call it 'active_subscribers']
    G --> H[Starting with cell A2 in 'original_subscribers_columnA_inserted.csv' starting with the number 1 and incrementing by 1 eacd row, add a sequentially unique number from cell A2 to the end of the active file which should be A'active_subscribers'
    H --> I[Save 'original_subscribers_columnA_inserted.csv']
