from app import create_app
from models import PatrimonyModel
from db import db
import os
import sqlite3
from excel_import import import_excel_data

app = create_app()
app.app_context().push()

# Substitua pelo caminho do arquivo Excel
excel_file = 'instance/bd.xlsx'

# Carregando os dados do arquivo Excel
data = import_excel_data(excel_file)

# Conectando-se ao banco de dados SQLite
sqlite_db = 'instance/data.db'

with sqlite3.connect(sqlite_db) as conn:
    cursor = conn.cursor()
    # Iterando sobre os dados do arquivo Excel
    for item in data:
        number, airport, description, price, responsible, registry, verified = item

        # Criando um novo objeto PatrimonyModel com os dados da linha
        patrimony = PatrimonyModel(number=number, airport=airport, description=description, price=price, responsible=responsible, registry=registry, verified=verified)

        # Adicionando o objeto ao banco de dados
        db.session.add(patrimony)

    # Realizando commit das alterações no banco de dados
    db.session.commit()

print("Dados importados com sucesso!")
