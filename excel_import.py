import pandas as pd

def import_excel_data(excel_file):
    df = pd.read_excel(excel_file, engine='openpyxl')

    data = []
    for index, row in df.iterrows():
        number = row['nr_patrimonio']
        airport = row['aeroporto']
        description = row['descricao_bem']
        price = row['valor']
        registry = row['matricula']
        responsible = row['responsavel']
        verified = False
        data.append((number, airport, description, price, responsible, registry, verified))

    return data
