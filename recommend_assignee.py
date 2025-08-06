import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from scipy.sparse import hstack
import numpy as np

# A. CARREGAR FERRAMENTAS E MODELO
# Carregamos o modelo treinado e os pré-processadores que guardámos
# Nota: Neste exemplo simplificado, estamos a re-criar as ferramentas
# para demonstração. Num projeto real, guardaríamos estes objetos
# como "vectorizer.pkl" e "mlb.pkl" para não ter que os re-criar.

# Carregar o DataFrame processado para obter os dados de treino para fit
df = pd.read_csv('processed_pandas_issues.csv')
df['body'] = df['body'].fillna('')
df['full_text'] = df['title'] + ' ' + df['body']

# Re-ajustar as ferramentas de pré-processamento
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X_text = vectorizer.fit_transform(df['full_text'])

df['labels'] = df['labels'].apply(eval)
mlb = MultiLabelBinarizer()
X_labels = mlb.fit_transform(df['labels'])

df['assignee_login'] = df['assignee_login'].fillna('unassigned')
X_assignee = pd.get_dummies(df['assignee_login'], prefix='assignee', dummy_na=False)

# Carregar o modelo treinado
model = joblib.load('random_forest_model_smote.pkl')

print("Modelo e ferramentas de pré-processamento carregadas com sucesso.")

# B. SIMULAR UMA NOVA ISSUE
# Vamos simular uma nova issue para o nosso modelo prever
new_issue = {
    'title': 'Add support for Python 3.11',
    'body': 'This is an urgent request to add support for the new Python version. It involves updating several dependencies and requires a deep knowledge of the project\'s core architecture.',
    'labels': ['enhancement', 'core-api'],
    'assignee_login': None # Nenhuma pessoa atribuída ainda
}

# C. PRÉ-PROCESSAR A NOVA ISSUE
# O pré-processamento deve ser exatamente o mesmo que fizemos para o treino
new_df = pd.DataFrame([new_issue])
new_df['body'] = new_df['body'].fillna('')
new_df['full_text'] = new_df['title'] + ' ' + new_df['body']

# 1. Vetorizar o texto da nova issue
new_X_text = vectorizer.transform(new_df['full_text'])

# 2. Codificar as labels da nova issue
new_X_labels = mlb.transform([new_issue['labels']])

# 3. Codificar o assignee da nova issue
# Cria um DataFrame de dummies para a nova issue, com as colunas do treino
new_X_assignee = pd.get_dummies(new_df['assignee_login'], prefix='assignee', dummy_na=False).reindex(
    columns=X_assignee.columns, fill_value=0
).values

# 4. Combinar todas as features da nova issue
new_X = hstack([new_X_text, new_X_labels, new_X_assignee])

# D. FAZER A PREVISÃO
# Usar o modelo treinado para prever se a issue será rápida ou lenta
prediction = model.predict(new_X)[0]
prediction_proba = model.predict_proba(new_X)[0]

print("\n--- Previsão do Modelo ---")
if prediction == 1:
    print("Previsão: Esta issue provavelmente será LENTA.")
    print(f"Probabilidade de ser Lenta: {prediction_proba[1]*100:.2f}%")
else:
    print("Previsão: Esta issue provavelmente será RÁPIDA.")
    print(f"Probabilidade de ser Rápida: {prediction_proba[0]*100:.2f}%")

# E. GERAR RECOMENDAÇÃO
# Geramos uma recomendação com base na nossa análise exploratória
top_assignees = df['assignee_login'].value_counts().nlargest(3).index.tolist()
if prediction == 1:
    print(f"\n--- Recomendação para a Issue ---")
    print("Como a issue é complexa e provavelmente lenta, recomendamos os colaboradores mais experientes:")
    print(f"-> Colaborador(es) recomendado(s): {', '.join(top_assignees)}")
else:
    print(f"\n--- Recomendação para a Issue ---")
    print("Como a issue é simples e provavelmente rápida, pode ser atribuída a um colaborador menos experiente para agilizar o fluxo.")