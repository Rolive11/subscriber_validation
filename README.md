# Subscriber Validation Repository

This repository contains tools and documentation for validating subscriber CSV files.

## Flowchart for Step 1 Validation
```mermaid
graph TD
    A[Start: Input Subscriber CSV File] --> B[Read CSV Headers]
    B --> C{Check for Exact Sequence of 12 Columns: <br>customer, lat, long, address, city, state, zip, <br>download, upload, voip_lines_quantity, <br>business_customer, technology}
    C -->|Found| D[Step 1: True - Exact Sequence Present]
    C -->|Not Found| E[Step 1: False - Sequence Missing or Incorrect]
    D --> F[Proceed to Next Validation Step]
    E --> G[Handle Missing/Incorrect Columns]