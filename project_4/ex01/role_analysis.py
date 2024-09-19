import os
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq


roles = {
    "Educador tradicional": "Você é um educador tradicional com anos de experiência em universidades convencionais. Analise a École 42 de uma perspectiva acadêmica.",
    "Estudante de tecnologia": "Você é um estudante de tecnologia ansioso para aprender programação. Analise a École 42 do ponto de vista de um potencial aluno.",
    "Recrutador de tecnologia": "Você é um recrutador de profissionais de uma grande empresa de tecnologia. Avalie a École 42 considerando as habilidades que você busca em candidatos."
}

user_prompt = "Descreva a École 42 e seu método de ensino. Destaque os pontos principais que seriam relevantes para sua perspectiva."

def gemini_prompt(system_prompt, user_prompt):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            f"Seja breve e imediato na resposta, e faça sem formatação. Com base nos dos dados: <roles>\n{system_prompt}</roles>\n\n{user_prompt}",
            generation_config=genai.GenerationConfig(
                max_output_tokens=50,
                temperature=1.0,
            ),
        )
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"

def groq_prompt(prompt):
    try:
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=1.0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling Groq API: {e}"

def query_models(system_prompt, user_prompt):
    gemini_response = gemini_prompt(system_prompt, user_prompt)
    groq_response = groq_prompt(user_prompt)
    
    return {
        "gemini": gemini_response,
        "groq": groq_response
    }

def main():
    load_dotenv()
    
    print("=== Análises usando GEMINI ===")
    for role, system_prompt in roles.items():
        responses = query_models(system_prompt, user_prompt)
        print(f"--- Análise da perspectiva de {role} ---")
        print(responses["gemini"])
        print()
    
    print("\n=== Análises usando LLAMA ===")
    for role, system_prompt in roles.items():
        responses = query_models(system_prompt, user_prompt)
        print(f"--- Análise da perspectiva de {role} ---")
        print({responses["groq"]})
        print()

if __name__ == "__main__":
    main()