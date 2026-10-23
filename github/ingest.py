import duckdb

# Conecta explicitamente ao ficheiro na raiz do projeto-2
con = duckdb.connect(r'C:/Users/Augusto/Projeto-2/financeiro.duckdb')

# Ingestão dos CSVs na pasta data/raw
con.execute("CREATE OR REPLACE TABLE raw_clientes AS SELECT * FROM read_csv_auto('data/raw/clientes.csv');")
con.execute("CREATE OR REPLACE TABLE raw_faturas AS SELECT * FROM read_csv_auto('data/raw/faturas.csv');")
con.execute("CREATE OR REPLACE TABLE raw_pagamentos AS SELECT * FROM read_csv_auto('data/raw/pagamentos.csv');")

print("✓ Tabelas brutas carregadas com sucesso no DuckDB!")
con.close()