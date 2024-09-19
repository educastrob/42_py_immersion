import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

def get_movie_info(query):
    user_prompt = f"""
	<role>
		He works as a renowned filmmaker who has been writing scripts and film reviews for over 20 years. You are discerning and know almost all of the films that have been released to date.
	</role>
	<objective>
		Provide information about the movie "{query}" in JSON format.
	</objective>
	<assistant_init>
		Start your response with:
		{{
		"title": {{"Movie Title"}},
	</assistant_init>
	<template>
		The answer must follow the template below. Return only the json as a response.
		{{
			"title": {{"Movie Title"}},
			"year": {{"0000"}},
			"director": {{"Director's Name"}},
			"genre": {{["Genre1", "Genre2"]}},
			"plot_summary": {{"Brief plot summary"}}
		}}
		<instructions>
			* Replacing {{"Movie Title"}} values ​​with the movie title the film;
			* Replacing {{"0000"}} values ​​with the year the film was released;
			* Replacing {{"Director's Name"}} values ​​with the name of the film's directors;
			* Replacing {{["Genre1", "Genre2"]}} values  with the genres that the film contains;
			* Replacing {{"Brief plot summary"}} values ​​with the brief of the film;
			* If you don't find any of the 5 pieces of information () return the string '#####' as input.
			* Please, review the json formatting in the final response. Don't forget to use commas as a separator and complete in pairs (open and close) all '{' '}' characters;
		</instructions>
	</template>
	<exemple>
		{{
			"title": {{"Barbie"}},
			"year": {{"2023"}},
			"director": {{"Greta Gerwig"}},
			"genre": {{["Fantasy", "Comedy"]}},
			"plot_summary": {{"In the colorful and seemingly perfect world of Barbie Land, Barbie and Ken enjoy their idyllic lives. However, when they venture into the real world, they encounter both the joys and challenges of living among humans."}}
		}}
	</exemple>
	"""
    return gemini_prompt(user_prompt)

def gemini_prompt(prompt):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=500,
                temperature=1.0,
            ),
        )
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"

movie_titles = ["The Matrix", "Inception", "Pulp Fiction", "The Shawshank Redemption", "The Godfather"]

def main():
	load_dotenv()
	for title in movie_titles:
		print(f"\nAnalyzing: {title}\n")
		result = get_movie_info(title)
		try:
			movie_info = json.loads(result)
			for key, value in movie_info.items():
				print(f"{key}: {value}")
		except json.JSONDecodeError:
			print("Error: Failed to generate valid JSON")
		print("-" * 50)
    
if __name__ == "__main__":
	main()
