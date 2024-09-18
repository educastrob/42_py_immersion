import os
import subprocess
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq

load_dotenv()

def format_prompt(job_description):
    prompt = f"Com base na seguinte descrição de vaga: {job_description}, elabore uma descrição concisa e precisa com base na primeira vaga de Engenharia de Software com mais informações que encontrar. Inclua informações sobre as ferramentas e habilidades técnicas requisitadas (exemplo: Python, Java, etc.). Formato da resposta:\n Name of role: [cargo]\nWorking hours: [horário]\nCountry: [país]\nTech skills: [habilidades técnicas]"
    return prompt

def gemini_prompt(prompt):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            max_output_tokens=300,
            temperature=1.0,
        ),
    )
    return response.text

def groq_prompt(prompt):
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=1.0
    )
    return response.choices[0].message.content

def ollama_prompt(prompt):
    comando = ["ollama", "run", "qwen2:1.5b"]
    try:
        resultado = subprocess.run(comando, input=prompt, capture_output=True, text=True, check=True)
        return resultado.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar o comando Ollama: {e}")
        return "Ocorreu um erro ao processar sua solicitação."

def query_all_models(formatted_prompt):
    print('Consultando Gemini...')
    print('Consultando Groq...')
    print('Consultando Ollama...')
    results = {}
    results['Gemini'] = gemini_prompt(formatted_prompt)
    results['Groq'] = groq_prompt(formatted_prompt)
    results['Ollama'] = ollama_prompt(formatted_prompt)
    return results

def main():
    with open("job_description.txt", "r") as file:
        job_description = file.read()
    formatted_prompt = format_prompt(job_description)
    results = query_all_models(formatted_prompt)
    for model, response in results.items():
        print(f"\nAnálise do {model}:")
        print(response)
        print("-" * 50)

if __name__ == "__main__":
    main()