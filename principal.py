from def_etl import extract
from def_etl import load
from def_etl import concatenar

# PASSO 1 - EXTRAIR OS DADOS
url_nba = "https://www.basketball-reference.com/friv/dailyleaders.fcgi?month=01&day=13&year=2024&type=all"
df_temp = extract(url_nba)

# PASSO 2 - CARREGAR OS ARQUIVOS
df_temp= load("C://Users//eduar//Desktop//NBA//db//database_temp.xlsx")
database = load("C://Users//eduar//Desktop//NBA//db//database.xlsx")

# PASSO 3 - CONCATENCAR OS ARQUIVOS
data = concatenar(database,df_temp)

print(data)
