import sys
import requests
from bs4 import BeautifulSoup

def should_include_title(title):
    # Adicione aqui a lógica para determinar se o título deve ser incluído
    # Por exemplo, você pode excluir títulos que contenham certas palavras
    return True

def roads_to_philosophy(search_term):
    visited_articles = set()
    base_url = "https://en.wikipedia.org"
    current_url = base_url + "/wiki/" + search_term.replace(' ', '_')

    while True:
        try:
            response = requests.get(current_url)
            response.raise_for_status()  # Raise an exception for error HTTP statuses

            soup = BeautifulSoup(response.content, 'html.parser')

            # Encontrar todos os links na área de conteúdo principal
            links = []
            for link in soup.select('#mw-content-text p a'):
                link_title = link.get('title')
                if link_title and should_include_title(link_title):
                    links.append(link)

            if links:
                next_link = links[0]  # Escolhe o primeiro link válido
                next_url = next_link.get('href')

                # Verifica se é um link relativo ou absoluto
                if next_url.startswith('/wiki/'):
                    next_url = base_url + next_url

                if next_url in visited_articles:
                    print("It leads to an infinite loop!")
                    break

                if 'Philosophy' in next_url:
                    link_counter = len(visited_articles) + 1
                    print("philosophy")
                    print(f"{link_counter} roads from {search_term} to philosophy!")
                    break

                visited_articles.add(next_url)
                current_url = next_url
                print(next_link.text)
            else:
                print("It leads to a dead end!")
                break

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}. Unable to continue.")
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Forneça um termo de busca como argumento.")
        sys.exit(1)

    search_term = sys.argv[1]
    roads_to_philosophy(search_term)