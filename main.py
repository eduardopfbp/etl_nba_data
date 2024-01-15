from def_etl import extract, load, concatenate

# STEP 1 - EXTRACT THE DATA
url_nba = "https://www.basketball-reference.com/friv/dailyleaders.fcgi?month=01&day=13&year=2024&type=all"
df_temp = extract(url_nba)

# STEP 2 - LOAD THE FILES
df_temp = load("C://Users//eduar//Desktop//NBA//db//database_temp.xlsx")
database = load("C://Users//eduar//Desktop//NBA//db//database.xlsx")

# STEP 3 - CONCATENATE THE FILES
data = concatenate(database, df_temp)

print(data)
