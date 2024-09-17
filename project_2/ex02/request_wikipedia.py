import requests
import json
import sys
import re
import unicodedata
from bs4 import BeautifulSoup


def wiki_text_formated(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    text_element = soup.find('p')
    text = text_element.get_text()
    return text

def request_wikipedia(search_term):

    url = f"https://pt.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={search_term}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        page_title = data['query']['search'][0]['title']

        page_url = f"https://pt.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=&titles={page_title}"
        page_response = requests.get(page_url)
        page_data = page_response.json()
        page_keys = list(page_data['query']['pages'].keys())
        page_content = page_data['query']['pages'][str(page_keys[0])]['extract']

        clean_filename = unicodedata.normalize('NFKD', page_title).encode('ascii', 'ignore').decode('ascii').replace(' ', '_')

        with open(f"{clean_filename}.wiki", 'w', encoding='utf-8') as f:
            f.write(wiki_text_formated(page_content))

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
