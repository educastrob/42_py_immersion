import requests
import json
import google.generativeai as genai

# API Key
genai.configure(api_key='AIzaSyA5yR5xbnzSbXWlkAKS_PaXKB6i44c6_6I')


model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content(
    "Escreva uma descrição precisa e breve de vaga real para um(a) [Pleno Software Engineer (BackEnd)] em uma empresa de [Tecnologia] em [Brasil]. Inclua informações sobre as ferramentas técnicas (Python, Java, etc.). Formato da resposta:\n Name of role: [cargo]\nWorking hours: [horário]\nCountry: [país]\nTech skills: [habilidades técnicas]",
    generation_config = genai.GenerationConfig(
        max_output_tokens = 300,
        temperature = 0.3,
    ),
)

with open("job_description.txt", "w") as f:
    f.write(response.text)
