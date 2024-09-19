import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()

def generate_response(prompt):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=1000,
                temperature=0.7,
            ),
        )
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"

def remove_xml_tags(text):
    return re.sub(r'<[^>]+>', '', text).strip()

def remove_objective_tag(text):
    return re.sub(r'<objective>.*?</objective>', '', text, flags=re.DOTALL).strip()

def shannon_analysis():
    # Etapa 1: Obter uma visão geral da vida e carreira de Claude Shannon
    prompt_stage_1 = f"""
    <stage>
        <objective>Forneça uma biografia detalhada de Claude Shannon, abrangendo sua formação acadêmica, carreira profissional, vida pessoal e principais interesses de pesquisa. Destaque os eventos e influências mais importantes que moldaram sua trajetória.</objective>
    </stage>
    """
    response_stage_1 = generate_response(prompt_stage_1)

    # Etapa 2: Analisar suas principais contribuições para a teoria da informação
    prompt_stage_2 = f"""
    <stage>
        <objective>Quais foram as principais contribuições de Claude Shannon para a teoria da informação? Explique em detalhes seus conceitos mais importantes, como entropia da informação, capacidade de canal e codificação, e como eles revolucionaram a forma como entendemos e processamos informações.</objective>
        <input>{response_stage_1}</input>
    </stage>
    """
    response_stage_2 = generate_response(prompt_stage_2)

    # Etapa 3: Explorar o impacto de seu trabalho na computação moderna e nas tecnologias de comunicação
    prompt_stage_3 = f"""
    <stage>
        <objective>De que forma o trabalho de Claude Shannon impactou o desenvolvimento da computação moderna e das tecnologias de comunicação? Explore como suas ideias foram aplicadas em áreas como teoria dos códigos, criptografia, compressão de dados e redes de comunicação.</objective>
        <input>{response_stage_2}</input>
    </stage>
    """
    response_stage_3 = generate_response(prompt_stage_3)

    prompt_stage_4 = f"""
    <stage>
        <objective>Sintetize as informações das etapas anteriores e apresente uma análise abrangente do legado de Claude Shannon. Qual é a importância duradoura de suas contribuições para a ciência da computação e para a sociedade em geral? Discuta o impacto de seu trabalho em áreas além da teoria da informação, como a inteligência artificial e a biologia.</objective>
        <input>{response_stage_3}</input>
    </stage>
    """
    
    response_stage_4 = generate_response(prompt_stage_4)
    result = remove_objective_tag(response_stage_4)

    return result

def run_prompt_chain():
    final_response = shannon_analysis()
    print(remove_xml_tags(final_response))

if __name__ == "__main__":
    run_prompt_chain()