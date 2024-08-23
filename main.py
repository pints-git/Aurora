from fastapi import FastAPI, Request
from transformers import pipeline
import requests
import os

app = FastAPI()

# Gen AI model
ai_model = pipeline("text-generation", model="gpt-3")

# OpenWeatherMap API
weather_api = "http://api.openweathermap.org/data/2.5/weather"

# NewsAPI
news_api = "https://newsapi.org/v2/top-headlines"

# Trivia API
trivia_api = "https://opentdb.com/api.php"

# API keys
weather_api_key = os.environ["WEATHER_API_KEY"]
news_api_key = os.environ["NEWS_API_KEY"]

# Chatbot
@app.post("/chat")
async def chat(request: Request):
    user_input = request.json()["user_input"]

    # Weather API
    if user_input == "weather":
        params = {"q": "London", "appid": weather_api_key}
        response = requests.get(weather_api, params=params).json()["weather"][0]["description"]
    # News API
    elif user_input == "news":
        params = {"country": "us", "apiKey": news_api_key}
        response = requests.get(news_api, params=params).json()["articles"][0]["title"]
    # Trivia API
    elif user_input == "trivia":
        params = {"amount": 1, "type": "multiple"}
        response = requests.get(trivia_api, params=params).json()["results"][0]["question"]
    # Customized response using Gen AI
    else:
        response = ai_model(user_input, max_length=50)["generated_text"]

    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
