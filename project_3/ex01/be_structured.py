import requests
import json
import google.generativeai as genai

# API Keys
genai.configure(api_key='AIzaSyA5yR5xbnzSbXWlkAKS_PaXKB6i44c6_6I')

def gemini_prompt():
    model = genai.GenerativeModel("gemini-1.5-flash")

    with open("job_description.txt", "r") as f:
        job_description = f.read()

    prompt = f"Com base na seguinte descrição de vaga: {job_description}, elabore uma descrição concisa e precisa com base na primeira vaga de Engenharia de Software com mais informações que encontrar. Inclua informações sobre as ferramentas e habilidades técnicas requisitadas (exemplo: Python, Java, etc.). Formato da resposta:\n Name of role: [cargo]\nWorking hours: [horário]\nCountry: [país]\nTech skills: [habilidades técnicas]"

    response = model.generate_content(
        prompt,
        generation_config = genai.GenerationConfig(
            max_output_tokens = 300,
            temperature = 1.0,
        ),
    )
    print(response.text)


def main():
    gemini_prompt()

if __name__ == '__main__':
    main()