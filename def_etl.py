import requests
from bs4 import BeautifulSoup
import pandas as pd

# EXTRACT 
def extract(url):
    
    # Send an HTTP request to the provided URL
    page = requests.get(url)

    # Check if the request was successful
    if page.status_code == 200:
        # Parse the content of the page using BeautifulSoup
        soup_nba = BeautifulSoup(page.content, 'html.parser')
        rows = soup_nba.findAll('tr')[1:]
        players_stats_2023 = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
        headers_2023 = [th.getText() for th in soup_nba.findAll('tr', limit=2)[0].findAll('th')]
        headers_2023_final = headers_2023[1:]
    else:
        print("Error in HTTP request.")

    # TRANSFORM
    # Create a DataFrame using the extracted data
    df = pd.DataFrame(players_stats_2023, columns=headers_2023_final)
    column_names = ['Player', 'Tm', 'Vs', 'Opp', 'Res', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', '+/-', 'GmSc']
    df.columns = column_names
    columns_to_remove = ['Vs', '+/-']
    df = df.drop(columns_to_remove, axis=1)
    df.set_index(headers_2023_final[0], inplace=True)

    # Extract year, month, and day from the URL
    data_str = url.split("?")[1]
    data_parts = data_str.split("&")
    year, month, day = None, None, None

    for part in data_parts:
        if part.startswith("year="):
            year = int(part.split("=")[1])
        elif part.startswith("month="):
            month = int(part.split("=")[1])
        elif part.startswith("day="):
            day = int(part.split("=")[1])

    # Add a new column with the date to the DataFrame
    df['Data'] = pd.to_datetime(f"{year}-{month}-{day}")

    # Handle Index (website issue)
    df = df[df.index.notna()]

    # Handle Null Values
    df.fillna(0, inplace=True)

    # Replace empty strings with '0' in percentage columns
    df['FG%'].replace('', '0', inplace=True)
    df['3P%'].replace('', '0', inplace=True)
    df['FT%'].replace('', '0', inplace=True)

    # Change Data Types
    dtype_change = {'Tm': str, 'Opp': str, 'Res': str, 'MP': object, 'FG': pd.Int64Dtype(), 'FGA': pd.Int64Dtype(), 'FG%': float, '3P': pd.Int64Dtype(),
                    '3PA': pd.Int64Dtype(), '3P%': float, 'FT': pd.Int64Dtype(), 'FTA': pd.Int64Dtype(), 'FT%': float, 'ORB': pd.Int64Dtype(),
                    'DRB': pd.Int64Dtype(), 'TRB': pd.Int64Dtype(), 'AST': pd.Int64Dtype(), 'STL': pd.Int64Dtype(), 'BLK': pd.Int64Dtype(),
                    'TOV': pd.Int64Dtype(), 'PF': pd.Int64Dtype(), 'PTS': pd.Int64Dtype(), 'GmSc': float, 'Data': str}

    df = df.astype(dtype_change)

    # If an error occurs, check here.
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce').dt.date
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce').dt.strftime('%Y-%m-%d')

    # Convert Minutes and Seconds
    df['MP'] = df['MP'].str.split(':').apply(lambda x: round(int(x[0]) + (int(x[1]) / 60), 2))
    
    # Export to Excel
    database = "C://Users//eduar//Desktop//NBA//db//database_temp.xlsx"
    df.to_excel(database)    
    
    return df

# TRANSFORM
def load(file):
    # Load the Excel file into a DataFrame
    file_ = pd.read_excel(file, engine='openpyxl')
    return file_

# CONCATENATE
def concatenate(base, temporary):
    base_ = base
    temp_ = temporary
    consolidated = pd.concat([base_, temp_])
    consolidated = consolidated.reset_index(drop=True)
    consolidated.to_excel("C://Users//eduar//Desktop//NBA//db//database.xlsx", index=False)
    
    return consolidated







