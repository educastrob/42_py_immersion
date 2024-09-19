import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

github_comments = [
    {
        "text": "Ótimo trabalho na implementação desta feature! O código está limpo e bem documentado. Isso vai ajudar muito nossa produtividade.",
        "sentiment": ""
    },
    {
        "text": "Esta mudança quebrou a funcionalidade X. Por favor, reverta o commit imediatamente.",
        "sentiment": ""
    },
    {
        "text": "Podemos discutir uma abordagem alternativa para este problema? Acho que a solução atual pode causar problemas de desempenho no futuro.",
        "sentiment": ""
    },
    {
        "text": "Obrigado por relatar este bug. Vou investigar e atualizar a issue assim que tiver mais informações.",
        "sentiment": ""
    },
    {
        "text": "Este pull request não segue nossas diretrizes de estilo de código. Por favor, revise e faça as correções necessárias.",
        "sentiment": ""
    },
    {
        "text": "Excelente ideia! Isso resolve um problema que estávamos enfrentando há semanas. Mal posso esperar para ver isso implementado.",
        "sentiment": ""
    },
    {
        "text": "Esta issue está aberta há meses sem nenhum progresso. Podemos considerar fechá-la se não for mais relevante?",
        "sentiment": ""
    },
    {
        "text": "O novo recurso está causando conflitos com o módulo Y. Precisamos de uma solução urgente para isso.",
        "sentiment": ""
    },
    {
        "text": "Boa captura! Este edge case não tinha sido considerado. Vou adicionar testes para cobrir este cenário.",
        "sentiment": ""
    },
    {
        "text": "Não entendo por que estamos priorizando esta feature. Existem problemas mais críticos que deveríamos estar abordando.",
        "sentiment": ""
    }
]

def call_llm(comments):
    examples = """
    <examples>
        <example>
            <text>O design da interface está incrível! Parabéns pelo excelente trabalho.</text>
            <sentiment>Positivo</sentiment>
        </example>
        <example>
            <text>Infelizmente, a última atualização introduziu vários bugs. Precisamos corrigir isso o mais rápido possível.</text>
            <sentiment>Negativo</sentiment>
        </example>
        <example>
            <text>O desempenho do sistema melhorou significativamente após as últimas otimizações. Bom trabalho!</text>
            <sentiment>Positivo</sentiment>
        </example>
        <example>
            <text>Podemos agendar uma reunião para discutir os próximos passos deste projeto?</text>
            <sentiment>Neutro</sentiment>
        </example>
        <example>
            <text>O código está bem organizado, mas acho que podemos simplificar algumas partes.</text>
            <sentiment>Positivo</sentiment>
        </example>
        <example>
            <text>Estou muito satisfeito com o progresso que fizemos até agora. Continuem assim!</text>
            <sentiment>Positivo</sentiment>
        </example>
        <example>
            <text>Precisamos melhorar a documentação do projeto. Está difícil entender algumas partes.</text>
            <sentiment>Negativo</sentiment>
        </example>
    </examples>
    """
    comments_xml = "\n".join([f"<text>{comment['text']}</text>" for comment in comments])
    prompt = f"Siga como os exemplos: {examples}\n<analyze>Agora analise os comentarios abaixo e os classifique como Positivo/Negativo/Neutro: \n{comments_xml}\n</analyze>"
    try:
        print("Consultando Gemini ...")
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Error in Gemini response."

def parse_llm_response(response):
    # Extrair o sentimento da resposta do modelo
    sentiments = []
    lines = response.split("\n")
    for line in lines:
        if "Positivo" in line:
            sentiments.append("Positivo")
        elif "Negativo" in line:
            sentiments.append("Negativo")
        elif "Neutro" in line:
            sentiments.append("Neutro")
    return sentiments

def analyze_sentiments(comments):
    llm_response = call_llm(comments)
    sentiments = parse_llm_response(llm_response)
    for comment, sentiment in zip(comments, sentiments):
        comment["sentiment"] = sentiment

analyze_sentiments(github_comments)

# Imprimir resultados
for comment in github_comments:
    print(f"Texto: {comment['text']}")
    print(f"Sentimento: {comment['sentiment']}")
    print()