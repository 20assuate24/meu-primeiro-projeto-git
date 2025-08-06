import requests
import json

# Repositório de exemplo com muitas issues para testar
owner = "pandas-dev"
repo = "pandas"

# URL da API para listar issues fechadas
# O parâmetro 'per_page=100' pede o máximo de issues por página (100)
url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=closed&per_page=100"

print(f"A chamar a API REST do GitHub para o repositório {owner}/{repo}...\n")

# Para evitar limites de taxa (rate limits) e acessar dados privados
# você precisaria de um token de acesso. Por agora, vamos tentar sem.
# headers = {"Authorization": "Bearer SEU_TOKEN_AQUI"}
# response = requests.get(url, headers=headers)
response = requests.get(url)

# Verificação se a chamada à API foi bem-sucedida (status code 200)
if response.status_code == 200:
    # A resposta JSON vem como uma lista de dicionários,
    # onde cada dicionário é uma issue.
    issues = response.json()
    
    print(f"Sucesso! Encontradas {len(issues)} issues na primeira página.")
    
    # Imprime a primeira issue da lista para ver a estrutura dos dados
    # O 'indent=2' formata o JSON para ser mais fácil de ler
    if issues:
        print("\n--- Estrutura da primeira issue ---\n")
        print(json.dumps(issues[0], indent=2))
    else:
        print("A API retornou uma lista vazia.")

else:
    print(f"Erro na chamada à API. Status Code: {response.status_code}")
    print(f"Resposta: {response.text}")