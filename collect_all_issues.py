import requests
import json
import time

owner = "pandas-dev"
repo = "pandas"

# Endereço base da API
base_url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=closed&per_page=100"

print("Iniciando a coleta de dados de issues...")

all_issues = []
page = 1

while True:
    url = f"{base_url}&page={page}"
    print(f"Buscando página {page}...")

    # Sem autenticação, o limite de requisições por hora é baixo.
    # Se der erro, pode ser o rate limit.
    response = requests.get(url)

    if response.status_code == 200:
        issues = response.json()
        if not issues:
            # Se a lista estiver vazia, significa que não há mais issues.
            break
        
        all_issues.extend(issues)
        print(f"Página {page} coletada. Total de issues até agora: {len(all_issues)}")
        page += 1
        
        # Pausa para não exceder o limite de requisições da API
        time.sleep(1) # Pausa de 1 segundo entre as requisições
        
    else:
        print(f"Erro na chamada da API na página {page}. Status Code: {response.status_code}")
        break

print(f"\nColeta de dados finalizada. Total de issues coletadas: {len(all_issues)}")

# O 'all_issues' agora contém todas as issues fechadas.
# Pode agora, por exemplo, guardar num ficheiro JSON
with open('all_pandas_issues.json', 'w', encoding='utf-8') as f:
    json.dump(all_issues, f, ensure_ascii=False, indent=4)

print("Dados salvos em 'all_pandas_issues.json'.")