# Sistema de Recomendação de Colaboradores para Issues

## Visão Geral do Projeto

Este projeto desenvolve um protótipo de um sistema de recomendação de colaboradores para issues do GitHub. A ferramenta utiliza dados históricos para prever a complexidade de novas issues e, com base nessa previsão, recomenda os colaboradores mais adequados para a sua resolução.

A base de dados utilizada consiste em 1.000 issues do repositório `pandas-dev/pandas`, coletadas através da API do GitHub.

## Motivação

O objetivo principal é otimizar o fluxo de trabalho de desenvolvimento. Atribuir a um colaborador sênior uma tarefa simples (rápida) é ineficiente, assim como atribuir uma tarefa complexa (lenta) a um colaborador júnior sem o devido suporte. Este sistema visa mitigar esses problemas, facilitando a gestão de tarefas.

## Estrutura do Repositório

* `collect_all_issues.py`: Script para coletar dados de issues da API do GitHub.
* `preprocess_issues.py`: Script de pré-processamento e limpeza dos dados brutos.
* `eda.py`: Script de Análise Exploratória de Dados.
* `feature_engineering.py`: Script para a criação de features a partir dos dados limpos.
* `model_training.py`: Script que treina e otimiza o modelo de Machine Learning (`RandomForestClassifier` com SMOTE).
* `recommend_assignee.py`: Script final que usa o modelo treinado para fazer previsões e recomendações.
* `relatorio_analise_exploratoria.md`: Relatório completo que documenta todas as fases do projeto.

## Tecnologias Utilizadas

* Python
* Pandas
* Scikit-learn
* `imblearn` (para SMOTE)
* `requests`
* `joblib`

## Resultados e Conclusões

O modelo inicial de `RandomForestClassifier` obteve uma acurácia de 70%, mas falhou em prever a classe minoritária ("lento") com um `recall` de apenas 21%. Para resolver este problema de desbalanceamento de classes, aplicámos o **SMOTE**, o que resultou numa melhoria significativa do `recall` para a classe "lento", que aumentou para **32%**.

A ferramenta final é capaz de:
1.  Prever se uma nova issue será "rápida" ou "lenta".
2.  Recomendar colaboradores experientes para issues complexas e colaboradores menos experientes para issues simples.

**Limitação Identificada:** O modelo é frágil a novos rótulos ou vocabulário que não foram observados nos dados de treino.

## Como Executar o Projeto

1.  Clone este repositório:
    ```bash
    git clone https://github.com/20assuate24/meu-primeiro-projeto-git.git
    ```
2.  Instale as dependências:
    ```bash
    pip install pandas scikit-learn imbalanced-learn requests
    ```
3.  Execute os scripts em ordem, do pré-processamento até a recomendação final:
    ```bash
    python collect_all_issues.py
    python preprocess_issues.py
    python eda.py
    python feature_engineering.py
    python model_training.py
    python recommend_assignee.py
    ```

---

### **Ação Final: Sincronizar o `README` com o GitHub**

Depois de atualizar o arquivo `README.md`, execute os comandos finais para enviar o trabalho para o GitHub.

```bash
git add README.md
git commit -m "docs: Adiciona README.md completo para documentar o projeto"
git push origin main