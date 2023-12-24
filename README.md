# NBA Player Statistics ETL Script

This Python script is designed to perform ETL (Extraction, Transformation, and Loading) operations on NBA player statistics data. The goal is to automate the process of updating player statistics, emphasizing proper data manipulation for subsequent analysis. The script addresses various considerations, including website issues, null values, and inconsistent data types.

## Features

- **Extraction (`extract` function):**
  - Utilizes `requests` and `BeautifulSoup` for making HTTP requests and extracting data from an HTML table.
  - Verifies the success of the request before processing the page content.
  - Converts extracted data into a pandas DataFrame, handling headers and values.

- **Transformation (Within the `extract` function):**
  - Renames columns.
  - Handles null values and problematic indices.
  - Converts specific data types for appropriate columns.
  - Exports the resulting DataFrame to an Excel file.

- **Loading (`load` and `concatenate` functions):**
  - `load` loads an existing Excel file into a DataFrame.
  - `concatenate` combines two DataFrames (one existing and one temporary), resetting the index, and exports the result to a new Excel file.
