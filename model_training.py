import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from scipy.sparse import hstack
from imblearn.over_sampling import SMOTE
import joblib

# Carregar o DataFrame processado
df = pd.read_csv('processed_pandas_issues.csv')
df['body'] = df['body'].fillna('')
df['full_text'] = df['title'] + ' ' + df['body']

# Vetorizar texto
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X_text = vectorizer.fit_transform(df['full_text'])

# Codificar 'labels'
df['labels'] = df['labels'].apply(eval)
mlb = MultiLabelBinarizer()
X_labels = mlb.fit_transform(df['labels'])

# Codificar 'assignee_login'
df['assignee_login'] = df['assignee_login'].fillna('unassigned')
X_assignee = pd.get_dummies(df['assignee_login'], prefix='assignee', dummy_na=False).values

# Combinar todas as features
X = hstack([X_text, X_labels, X_assignee])
y = (df['time_to_close_days'] > 5).astype(int) # Variável alvo: 1 para lento, 0 para rápido

print("Dados preparados para o treino do modelo.")
print(f"Shape de X: {X.shape}, Shape de y: {y.shape}")

# Dividir os dados em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- NOVA ETAPA: Balancear os dados de treino com SMOTE ---
print("\nBalanceando os dados de treino com SMOTE...")
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

print("Dados de treino balanceados.")
print(f"Shape do conjunto de treino original: {X_train.shape}")
print(f"Shape do conjunto de treino balanceado: {X_train_res.shape}")

# Treinar o modelo com os dados balanceados
model = RandomForestClassifier(n_estimators=100, random_state=42)
print("\nIniciando o treino do modelo RandomForest com dados balanceados...")
model.fit(X_train_res, y_train_res)
print("Treino do modelo concluído!")

# Fazer previsões no conjunto de teste (original, sem SMOTE) e avaliar
y_pred = model.predict(X_test)

print("\n--- Relatório de Classificação (com SMOTE) ---")
print(classification_report(y_test, y_pred))

# Opcional: Salvar o novo modelo treinado
joblib.dump(model, 'random_forest_model_smote.pkl')
print("\nNovo modelo salvo em 'random_forest_model_smote.pkl'.")