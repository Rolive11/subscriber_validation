# Subscriber Validation Repository

This repository contains tools and documentation for validating subscriber CSV files.

## Flowchart for Step 1 Validation
```mermaid
graph TD
    A[Start: Run python3 vs.py "original_subscriber.csv" "company_id"] --> B[Create directory "company_id"]
    B --> C[Save "original_subscribers.csv" in "company_id"]
    C --> D[Create "original_subscribers_columnA_inserted.csv"]
    D --> E[Copy content to "original_subscribers_columnA_inserted.csv"]
    E --> F[Insert column left of A and save]
    F --> G[Count rows with data in column B from row 2, call it "active_subscribers"]
    G --> H[Add sequential numbers from 1 in A2 to A"active_subscribers"]
    H --> I[Save "original_subscribers_columnA_inserted.csv"]
