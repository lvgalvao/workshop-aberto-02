import os
import gdown
import duckdb
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

# Carrega as variáveis de ambiente
load_dotenv()

def conectar_banco():
    """Conecta ao banco de dados DuckDB; cria o banco se não existir."""
    return duckdb.connect(database='duckdb.db', read_only=False)

def inicializar_tabela(con):
    """Cria a tabela se ela não existir."""
    con.execute("""
        CREATE TABLE IF NOT EXISTS historico_arquivos (
            nome_arquivo VARCHAR,
            horario_processamento TIMESTAMP
        )
    """)

def registrar_arquivo(con, nome_arquivo):
    """Registra um novo arquivo no banco de dados com o horário atual."""
    con.execute("""
        INSERT INTO historico_arquivos (nome_arquivo, horario_processamento)
        VALUES (?, ?)
    """, (nome_arquivo, datetime.now()))

def arquivos_processados(con):
    """Retorna um set com os nomes de todos os arquivos já processados."""
    return set(row[0] for row in con.execute("SELECT nome_arquivo FROM historico_arquivos").fetchall())

def baixar_pasta_google_drive(url_pasta, diretorio_local):
    os.makedirs(diretorio_local, exist_ok=True)
    gdown.download_folder(url_pasta, output=diretorio_local, quiet=False, use_cookies=False)

def listar_arquivos_e_tipos(diretorio):
    """Lista arquivos e identifica se são CSV, JSON ou Parquet."""
    arquivos_e_tipos = []
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".csv") or arquivo.endswith(".json") or arquivo.endswith(".parquet"):
            caminho_completo = os.path.join(diretorio, arquivo)
            tipo = arquivo.split(".")[-1]
            arquivos_e_tipos.append((caminho_completo, tipo))
    return arquivos_e_tipos

def ler_arquivo(caminho_do_arquivo, tipo):
    """Lê o arquivo de acordo com seu tipo e retorna um DataFrame."""
    if tipo == 'csv':
        return duckdb.read_csv(caminho_do_arquivo)
    elif tipo == 'json':
        return pd.read_json(caminho_do_arquivo)
    elif tipo == 'parquet':
        return pd.read_parquet(caminho_do_arquivo)
    else:
        raise ValueError(f"Tipo de arquivo não suportado: {tipo}")

def transformar(df):
    # Executa a consulta SQL que inclui a nova coluna, operando sobre a tabela virtual
    df_transformado = duckdb.sql("SELECT *, quantidade * valor AS total_vendas FROM df").df()
    # Remove o registro da tabela virtual para limpeza
    print(df_transformado)
    return df_transformado

def salvar_no_postgres(df, tabela):
    """Salva o DataFrame no PostgreSQL."""
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    df.to_sql(tabela, con=engine, if_exists='append', index=False)

def pipeline():
    url_pasta = 'https://drive.google.com/drive/folders/19flL9P8UV9aSu4iQtM6Ymv-77VtFcECP'
    diretorio_local = './pasta_gdown'

    # baixar_pasta_google_drive(url_pasta, diretorio_local)
    con = conectar_banco()
    inicializar_tabela(con)
    processados = arquivos_processados(con)
    arquivos_e_tipos = listar_arquivos_e_tipos(diretorio_local)

    logs = []
    for caminho_do_arquivo, tipo in arquivos_e_tipos:
        nome_arquivo = os.path.basename(caminho_do_arquivo)
        if nome_arquivo not in processados:
            df = ler_arquivo(caminho_do_arquivo, tipo)
            df_transformado = transformar(df)
            salvar_no_postgres(df_transformado, "vendas_calculado")
            registrar_arquivo(con, nome_arquivo)
            print(f"Arquivo {nome_arquivo} processado e salvo.")
            logs.append(f"Arquivo {nome_arquivo} processado e salvo.")

        else:
            print(f"Arquivo {nome_arquivo} já foi processado anteriormente.")
            logs.append(f"Arquivo {nome_arquivo} já foi processado anteriormente.")

    return logs
    

if __name__ == "__main__":
    pipeline()
