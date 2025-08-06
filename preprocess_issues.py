import pandas as pd
import json
import numpy as np

# 1. Carregar os dados do arquivo JSON
with open('all_pandas_issues.json', 'r', encoding='utf-8') as f:
    issues_data = json.load(f)

# 2. Converter os dados para um DataFrame do Pandas
df = pd.DataFrame(issues_data)

print("DataFrame criado com sucesso!")
print(f"Número de linhas (issues): {df.shape[0]}")
print(f"Número de colunas: {df.shape[1]}")
print("\nColunas originais:")
print(df.columns.tolist())

# 3. Selecionar as colunas relevantes
cols_to_keep = ['number', 'title', 'body', 'labels', 'assignee', 'created_at', 'closed_at']
df_filtered = df[cols_to_keep].copy()

# 4. Pré-processamento das colunas
df_filtered['assignee_login'] = df_filtered['assignee'].apply(
    lambda x: x['login'] if isinstance(x, dict) and 'login' in x else None
)
df_filtered['labels'] = df_filtered['labels'].apply(
    lambda x: [label['name'] for label in x] if isinstance(x, list) else []
)

# 5. Calcular o tempo de conclusão da tarefa
df_filtered['created_at'] = pd.to_datetime(df_filtered['created_at'])
df_filtered['closed_at'] = pd.to_datetime(df_filtered['closed_at'])
df_filtered['time_to_close_days'] = (df_filtered['closed_at'] - df_filtered['created_at']).dt.total_seconds() / (60*60*24)

# Exibir as primeiras linhas do DataFrame processado
print("\nDataFrame processado (primeiras 5 linhas):")
print(df_filtered.head())
print("\nInformações sobre as colunas do DataFrame processado:")
print(df_filtered.info())

# 6. Salvar o DataFrame processado em um novo arquivo CSV
df_filtered.to_csv('processed_pandas_issues.csv', index=False, encoding='utf-8')
print("\nDataFrame processado salvo em 'processed_pandas_issues.csv'.")