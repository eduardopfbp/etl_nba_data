import requests
from bs4 import BeautifulSoup
import pandas as pd

# EXTRACT 
def extract(url):
    
    page = requests.get(url)

    # Verificar se a solicitação foi bem-sucedida
    if page.status_code == 200:
        # Analisar o conteúdo da página com BeautifulSoup
        soup_nba = BeautifulSoup(page.content, 'html.parser')
        rows = soup_nba.findAll('tr')[1:]
        players_stats_2023 = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
        headers_2023 = [th.getText() for th in soup_nba.findAll('tr', limit=2)[0].findAll('th')]
        headers_2023_final = headers_2023[1:]
    else:
        print("Erro na solicitação HTTP.")

    # TRANSFORM
    df = pd.DataFrame(players_stats_2023,columns=headers_2023_final)
    nomes_colunas = ['Player', 'Tm', 'Vs', 'Opp', 'Res', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA','3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK','TOV', 'PF', 'PTS', '+/-', 'GmSc']
    df.columns = nomes_colunas
    remover_colunas = ['Vs','+/-']
    df = df.drop(remover_colunas, axis=1)
    df.set_index(headers_2023_final[0], inplace= True)

    data_str = url.split("?")[1]  # Pega a parte da URL após o ponto de interrogação
    data_parts = data_str.split("&")  # Divide os parâmetros da URL

    # Inicializar as variáveis para o ano, mês e dia
    ano = None
    mes = None
    dia = None

# Procurar pelos parâmetros de ano, mês e dia na URL
    for part in data_parts:
        if part.startswith("year="):
            ano = int(part.split("=")[1])
        elif part.startswith("month="):
            mes = int(part.split("=")[1])
        elif part.startswith("day="):
            dia = int(part.split("=")[1])

    # Criar uma nova coluna no DataFrame com a data
    df['Data'] = pd.to_datetime(f"{ano}-{mes}-{dia}")

    # Tratamento de Index ( problema do SITE )
    df = df[df.index.notna()]

    # Tratamento de Valroes Nulos
    df.fillna(0, inplace=True)

    df['FG%'].replace('', '0', inplace=True)
    df['3P%'].replace('', '0', inplace=True)
    df['FT%'].replace('', '0', inplace=True)


    # Tratamento to de Dtype
    dtype_change = {'Tm':str,'Opp':str,'Res':str,'MP':object,'FG':pd.Int64Dtype(),'FGA':pd.Int64Dtype(),'FG%':float,'3P':pd.Int64Dtype(),'3PA':pd.Int64Dtype(),
                        '3P%':float,'FT':pd.Int64Dtype(),'FTA':pd.Int64Dtype(),'FT%':float,'ORB':pd.Int64Dtype(),'DRB':pd.Int64Dtype(),'TRB':pd.Int64Dtype(),'AST':pd.Int64Dtype(),'STL':pd.Int64Dtype(),'BLK':pd.Int64Dtype(),
                        'TOV':pd.Int64Dtype(),'PF':pd.Int64Dtype(),'PTS':pd.Int64Dtype(),'GmSc':float,'Data':str}

    df = df.astype(dtype_change)

    # Caso der erro, verificar por aqui.
    #df['Data'] = pd.to_datetime(df['Data'], infer_datetime_format=True, errors='coerce')
    #df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce').dt.date
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce').dt.strftime('%Y-%m-%d')


    # Transformando os Minutos e Segundos
    df['MP'] = df['MP'].str.split(':').apply(lambda x: round(int(x[0]) + (int(x[1]) / 60),2))
    
    
    # Exportando
    database = "C://Users//eduar//Desktop//NBA//db//database_temp.xlsx"

    df.to_excel(database)    
    
    return df




# TRANSFORM

def load(arquivo):
    # Carrega o arquivo Excel em um DataFrame
    arquivo_ = pd.read_excel(arquivo, engine='openpyxl')
    # Usar apenas para os corrompidos com duplo índice
    #arquivo_ = arquivo_.drop(arquivo_.columns[:1], axis=1)
    return arquivo_




# CONCANTENCAR


def concatenar(base,temporario):

    base_ = base
    temp_ = temporario
    consolidado = pd.concat([base_,temp_])
    consolidado = consolidado.reset_index(drop=True)
    consolidado.to_excel("C://Users//eduar//Desktop//NBA//db//database.xlsx", index=False)
    

    return consolidado






