# Relatório de Análise Exploratória de Dados (AED)

## Sumário das Conclusões

### 1. Conclusões sobre a Distribuição do Tempo de Conclusão

- A maioria das issues (aproximadamente 650) é fechada em menos de 10 dias, indicando um alto volume de tarefas rápidas.
- O tempo de conclusão tem uma distribuição "cauda longa", com algumas issues demorando até 192 dias para serem fechadas.
- Hipótese para o modelo: podemos tratar a previsão do tempo de conclusão como um problema de **classificação**, onde a variável alvo é se uma issue será fechada "rápido" (e.g., < 5 dias) ou "lento" (> 5 dias).
![alt text](image-1.png)
### 2. Conclusões sobre os Colaboradores
- A análise dos colaboradores mostra uma distribuição desigual de atribuições.
- Os colaboradores `arthurlw` e `chilin0525` são os mais ativos, lidando com um número significativamente maior de issues.
- A variável `assignee_login` será uma feature muito importante no nosso modelo, pois alguns colaboradores parecem ser mais especializados ou produtivos.
![alt text](image.png)
## Próximos Passos
- Prosseguir com a Fase 4: Preparação dos Dados para o Modelo.
- Executar o script `feature_engineering.py` para vetorizar texto e codificar variáveis categóricas.

### 3. Conclusões sobre o Treino e Avaliação do Modelo Inicial

- **Performance do Modelo:** O modelo `RandomForestClassifier` atingiu uma acurácia de 70% no conjunto de teste, o que é um bom resultado inicial.
- **Desbalanceamento de Classes:** Identificámos um desbalanceamento no dataset, onde a maioria das issues é resolvida rapidamente. O conjunto de teste continha mais issues da classe "rápido" do que da classe "lento".
- **Limitações do Modelo:** O modelo é muito bom a prever issues rápidas (`recall` de 95%), mas tem um desempenho insatisfatório a prever issues lentas (`recall` de 21%).
- **Próximos Passos (para o Modelo):** Precisamos de abordar o desbalanceamento das classes para melhorar a capacidade do modelo de identificar issues que levam mais tempo a ser concluídas.

 python model_training.py
Dados preparados para o treino do modelo.
Shape de X: (1000, 1153), Shape de y: (1000,)

Dados divididos em conjuntos de treino e teste.
Shape do conjunto de treino (X_train): (800, 1153)
Shape do conjunto de teste (X_test): (200, 1153)

Iniciando o treino do modelo RandomForest...
Treino do modelo concluído!

--- Relatório de Classificação ---
              precision    recall  f1-score   support

           0       0.70      0.95      0.81       132
           1       0.70      0.21      0.32        68

    accuracy                           0.70       200
   macro avg       0.70      0.58      0.56       200
weighted avg       0.70      0.70      0.64       200


Modelo salvo em 'random_forest_model.pkl'.

Iniciando o treino do modelo RandomForest...
Treino do modelo concluído!

--- Relatório de Classificação ---
              precision    recall  f1-score   support

           0       0.70      0.95      0.81       132
           1       0.70      0.21      0.32        68

    accuracy                           0.70       200
   macro avg       0.70      0.58      0.56       200
weighted avg       0.70      0.70      0.64       200


Modelo salvo em 'random_forest_model.pkl'.
   macro avg       0.70      0.58      0.56       200
weighted avg       0.70      0.70      0.64       200


Modelo salvo em 'random_forest_model.pkl'.

Modelo salvo em 'random_forest_model.pkl'.

### 4. Melhoria do Modelo: Uso de SMOTE para Balanceamento de Classes

- **Estratégia:** Para abordar o fraco desempenho do modelo na classe minoritária ("lento"), foi utilizada a técnica de sobreamostragem SMOTE (Synthetic Minority Over-sampling Technique) nos dados de treino.
- **Resultados:** O uso de SMOTE resultou numa melhoria significativa do `recall` para a classe "lento", que aumentou de 21% para 32%.
- **Conclusão:** O modelo agora demonstra uma capacidade superior para identificar as issues que demoram mais tempo a ser fechadas, o que é um resultado crucial para o objetivo do projeto. Esta melhoria ocorreu com uma ligeira diminuição da acurácia geral, um tradeoff aceitável para aumentar a eficácia nas previsões mais relevantes.

Dados preparados para o treino do modelo.
Shape de X: (1000, 1153), Shape de y: (1000,)

Balanceando os dados de treino com SMOTE...
Dados de treino balanceados.
Shape do conjunto de treino original: (800, 1153)
Shape do conjunto de treino balanceado: (1110, 1153)

Iniciando o treino do modelo RandomForest com dados balanceados...
Treino do modelo conclu�do!

--- Relat�rio de Classifica��o (com SMOTE) ---
              precision    recall  f1-score   support

           0       0.70      0.83      0.76       132
           1       0.49      0.32      0.39        68

    accuracy                           0.66       200
   macro avg       0.60      0.57      0.57       200
weighted avg       0.63      0.66      0.63       200

### 5. Resultados finais do projecto
O nosso sistema de recomendação funciona, mas tem uma limitação crítica: ele é frágil a novas informações. Se uma nova issue tiver palavras ou rótulos que não estavam no nosso conjunto de treino, o modelo não vai conseguir usá-los para fazer a previsão.

$ python recommend_assignee.py
Modelo e ferramentas de pré-processamento carregadas com sucesso.
$ python recommend_assignee.py
Modelo e ferramentas de pré-processamento carregadas com sucesso.
C:\Users\SWIFT\anaconda3\Lib\site-packages\sklearn\preprocessing\_label.py:900: UserWarning: unknown class(es) ['core-api', 'enhancement'] will be igModelo e ferramentas de pré-processamento carregadas com sucesso.
C:\Users\SWIFT\anaconda3\Lib\site-packages\sklearn\preprocessing\_label.py:900: UserWarning: unknown class(es) ['core-api', 'enhancement'] will be igC:\Users\SWIFT\anaconda3\Lib\site-packages\sklearn\preprocessing\_label.py:900: UserWarning: unknown class(es) ['core-api', 'enhancement'] will be ignored
  warnings.warn(

  warnings.warn(

--- Previsão do Modelo ---

--- Previsão do Modelo ---
Previsão: Esta issue provavelmente será RÁPIDA.
--- Previsão do Modelo ---
Previsão: Esta issue provavelmente será RÁPIDA.
Probabilidade de ser Rápida: 65.00%
Previsão: Esta issue provavelmente será RÁPIDA.
Probabilidade de ser Rápida: 65.00%

--- Recomendação para a Issue ---
Probabilidade de ser Rápida: 65.00%

--- Recomendação para a Issue ---

--- Recomendação para a Issue ---
Como a issue é simples e provavelmente rápida, pode ser atribuída a um colaborador menos experiente para agilizar o fluxo.
--- Recomendação para a Issue ---
Como a issue é simples e provavelmente rápida, pode ser atribuída a um colaborador menos experiente para agilizar o fluxo.
Como a issue é simples e provavelmente rápida, pode ser atribuída a um colaborador menos experiente para agilizar o fluxo.