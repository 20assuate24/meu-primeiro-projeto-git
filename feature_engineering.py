import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from scipy.sparse import hstack
import numpy as np

# Carregar o DataFrame processado
df = pd.read_csv('processed_pandas_issues.csv')

# Preencher valores ausentes no corpo (body) com uma string vazia
df['body'] = df['body'].fillna('')

# 1. Combinar e vetorizar o texto
df['full_text'] = df['title'] + ' ' + df['body']
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X_text = vectorizer.fit_transform(df['full_text'])
print("Texto vetorizado usando TF-IDF.")

# 2. Codificar a variável 'labels'
df['labels'] = df['labels'].apply(eval)  # Converter a string de lista para uma lista real
mlb = MultiLabelBinarizer()
X_labels = mlb.fit_transform(df['labels'])
print("Labels codificadas usando MultiLabelBinarizer.")

# 3. Codificar a variável 'assignee_login'
df['assignee_login'] = df['assignee_login'].fillna('unassigned')
X_assignee = pd.get_dummies(df['assignee_login'], prefix='assignee', dummy_na=False).values
print("Assignee_login codificado usando One-Hot Encoding.")

# 4. Criar a variável alvo (y)
# Vamos classificar como "rápido" (0) se fechado em menos de 5 dias, e "lento" (1) caso contrário.
df['is_slow_to_close'] = (df['time_to_close_days'] > 5).astype(int)
y = df['is_slow_to_close']

# 5. Combinar todas as features em uma única matriz
X = hstack([X_text, X_labels, X_assignee])

print(f"\nShape final da matriz de features (X): {X.shape}")
print(f"Shape final da variável alvo (y): {y.shape}")

# O nosso dataset agora está pronto para a modelagem de Machine Learning!
# O nosso próximo passo será dividir X e y em conjuntos de treino e teste e treinar um modelo.