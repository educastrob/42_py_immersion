import requests
from bs4 import BeautifulSoup

url = "https://www.linkedin.com/jobs/search?keywords=python%20developer&location=São%20Paulo"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Identifica os elementos HTML que contêm as informações das vagas
    jobs = soup.find_all('div', class_='base-card')

    # Abrir o arquivo para escrita
    with open('job_description.txt', 'w', encoding='utf-8') as file:
        for job in jobs:
            # Escrever o conteúdo HTML do base-card no arquivo
            file.write(job.prettify() + '\n\n')

    print("Conteúdo dos base-cards copiado para job_description.txt")
else:
    print(f"Erro na requisição: {response.status_code}")