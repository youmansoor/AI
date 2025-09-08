# chatbot.py
import random
from datetime import datetime
import requests
import openai
import os

# Set your OpenAI API key (safely!)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Fun facts and jokes
jokes = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why did the math book look sad? Because it had too many problems.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I'm reading a book about anti-gravity. It's impossible to put down!"
]

fun_facts = [
    "Honey never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs that still tasted good.",
    "Octopuses have three hearts.",
    "Bananas are berries, but strawberries aren't.",
    "Your heart beats over 100,000 times a day."
]

# GPT fallback
def gpt_fallback(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're ChatPy, a witty and clever assistant."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.8,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except:
        return "I'm having a bit of a brain freeze. Try again in a sec!"

# Weather
def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")  # Set this in your environment
    if not api_key:
        return "Weather API key not set."
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        data = requests.get(url).json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"The weather in {city.title()} is {temp}°C with {desc}."
    except:
        return "Couldn't fetch the weather. Storm in my brain?"

# Main response logic
def chatbot_response(user_input):
    user_input = user_input.lower().strip()

    if "hi" in user_input or "hello" in user_input:
        return "Hey there, superstar! 🌟 What can I do for you?"

    elif "how are you" in user_input:
        return "Living my best virtual life. Thanks for asking!"

    elif "joke" in user_input:
        return random.choice(jokes)

    elif "fact" in user_input:
        return random.choice(fun_facts)

    elif "flip a coin" in user_input:
        return f"It's {'Heads' if random.choice([True, False]) else 'Tails'}! 🪙"

    elif "roll a dice" in user_input or "roll a die" in user_input:
        return f"You rolled a {random.randint(1, 6)} 🎲"

    elif "time" in user_input:
        return f"The time is {datetime.now().strftime('%I:%M %p')}."

    elif "date" in user_input or "today" in user_input:
        return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."

    elif "weather in" in user_input:
        city = user_input.split("weather in")[-1].strip()
        return get_weather(city)

    elif "help" in user_input:
        return (
            "Here's what I can do:\n"
            "- Tell jokes 🤪\n"
            "- Fun facts 🧠\n"
            "- Flip coins, roll dice 🎲\n"
            "- Show time/date ⏰\n"
            "- Weather in your city ☁️\n"
            "- Chat using GPT 🤖\n"
            "Try asking me something!"
        )

    # Fallback to GPT
    else:
        return gpt_fallback(user_input)