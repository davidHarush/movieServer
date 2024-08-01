import os

import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


def call_openai_api(api_key, question, max_tokens):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": question}],
        "max_tokens": max_tokens
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"


def movie_insights(api_key, movies):
    question = f"Please give me insights about my favorite movies: {', '.join(movies)}."
    return call_openai_api(api_key, question, 150)


def recommend_5_movies(api_key, movies):
    question = f"Recommend 5 movies based on the following list: {', '.join(movies)}. Provide only the list of movie titles."
    response_text = call_openai_api(api_key, question, 100)

    if "Error" in response_text:
        return response_text

    recommended_movies = [movie.strip() for movie in response_text.split("\n") if movie.strip()]
    return recommended_movies


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    movies = data.get('movies', [])
    api_key = data.get('api_key', os.getenv("OPENAI_API_KEY"))
    if not movies or not api_key:
        return jsonify({"error": "Movies or API key not provided"}), 400

    analysis = movie_insights(api_key, movies)
    recommendations = recommend_5_movies(api_key, movies)
    return jsonify({"analysis": analysis, "recommendations": recommendations}), 200


def test_analyze_taste():
    test_movies = ["Inception", "Titanic", "The Dark Knight", "Interstellar", "The Godfather"]

    with app.test_client() as client:
        response = client.post('/analyze', json={"movies": test_movies, "api_key": api_key})
        print("Test Response:", response.get_json())


if __name__ == '__main__':
    test_analyze_taste()

    app.run(debug=True)