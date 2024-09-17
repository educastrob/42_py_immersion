import requests
import json
import sys
import re
import unicodedata
from bs4 import BeautifulSoup

#### LEMBRAR DE CRIAR REQUIREMENTS.TXT ####

def request_wikipedia(search_term):
    """
    Faz uma busca na Wikipédia e salva o resultado em um arquivo.

    Args:
        search_term (str): O termo de busca.
    """

    # Construindo a URL da API da Wikipédia
    url = f"https://pt.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={search_term}"

    try:
        # Fazendo a requisição
        response = requests.get(url)
        response.raise_for_status()  # Lança exceção para status HTTPs inválidos

        # Parseando a resposta JSON
        data = response.json()
        page_title = data['query']['search'][0]['title']

        # Fazendo uma nova requisição para obter o conteúdo da página
        page_url = f"https://pt.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=&titles={page_title}"
        page_response = requests.get(page_url)
        page_data = page_response.json()
        page_keys = list(page_data['query']['pages'].keys())
        page_content = page_data['query']['pages'][str(page_keys[0])]['extract']
        
        soup = BeautifulSoup(page_content, 'html.parser')
        text_element = soup.find('p')
        text = text_element.get_text()

        # Limpando o nome do arquivo
        clean_filename = unicodedata.normalize('NFKD', page_title).encode('ascii', 'ignore').decode('ascii').replace(' ', '_')

        # Salvando o conteúdo em um arquivo
        with open(f"{clean_filename}.wiki", 'w', encoding='utf-8') as f:
            f.write(text)

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
    except KeyError as e:
        print(f"Erro ao processar a resposta: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
		
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Forneça um termo de busca como argumento.")
        sys.exit(1)

    search_term = sys.argv[1]
    request_wikipedia(search_term)
