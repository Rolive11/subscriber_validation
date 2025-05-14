# Subscriber Validation Repository

This repository contains tools and documentation for validating subscriber CSV files.

## Flowchart for Step 1 Validation
```mermaid
graph TD
    A[Start: Input the Subscriber CSV File and Company ID] --> B[Create or Overwrite a Directory called 'ID' off of the main directory, where ID is the imported Company ID] 
    B --> C[Save the Original Subscribers file in the new directory] 
    C --> D[Create a new csv file called Column_Retained and add it to the 'ID' directory] 
    D --> E[Copy the contents of the Original Subscribers file to theis new csv file and then insert one column to the left of Column A and save the file]
