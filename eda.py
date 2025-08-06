import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carregar os dados limpos do arquivo CSV
df = pd.read_csv('processed_pandas_issues.csv')

print("DataFrame carregado com sucesso para a Análise Exploratória.")
print(f"Número de linhas: {df.shape[0]}")

# 2. Análise da distribuição do tempo de conclusão (time_to_close_days)
print("\nAnálise da coluna 'time_to_close_days':")
print(df['time_to_close_days'].describe())

# Gerar um histograma para visualizar a distribuição
plt.figure(figsize=(10, 6))
sns.histplot(df['time_to_close_days'].dropna(), bins=50, kde=True)
plt.title('Distribuição do Tempo de Conclusão das Issues (em dias)')
plt.xlabel('Tempo para Conclusão (dias)')
plt.ylabel('Contagem')
plt.xlim(0, df['time_to_close_days'].quantile(0.99)) # Limita o eixo X para melhor visualização
plt.show()

# 3. Análise dos colaboradores mais ativos
top_assignees = df['assignee_login'].value_counts().nlargest(10)
print("\nTop 10 Colaboradores por número de Issues:")
print(top_assignees)

# Gerar um gráfico de barras para os top 10 colaboradores
plt.figure(figsize=(12, 7))
sns.barplot(x=top_assignees.values, y=top_assignees.index)
plt.title('Top 10 Colaboradores com mais Issues Atribuídas')
plt.xlabel('Número de Issues')
plt.ylabel('Colaborador')
plt.show()


