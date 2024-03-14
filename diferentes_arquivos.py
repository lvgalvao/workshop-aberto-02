import duckdb

def csv_to_parquet(csv_file_path, parquet_file_path):
    df = duckdb.read_csv(csv_file_path)
    df.to_parquet(parquet_file_path)

def parquet_to_csv(parquet_file_path):
    df = duckdb.read_parquet(parquet_file_path)
    df.to_csv("arquivo.csv")

def json_to_csv(json_file_path, csv_file_path):
    df = duckdb.read_json(json_file_path)
    df.to_csv(csv_file_path, index=False)

# Exemplo de uso:
csv_file = 'pasta_gdown/vendas_08_01_2024.csv'
parquet_file = 'pasta_gdown/vendas_08_01_2024.parquet'

parquet_to_csv(parquet_file)
