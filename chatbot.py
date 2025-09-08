import random
from datetime import datetime
import requests
import difflib

# Jokes
jokes = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why did the math book look sad? Because it had too many problems.",
    "Why don’t skeletons fight each other? They don’t have the guts.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!"
]

# Fun facts
fun_facts = [
    "Honey never spoils. Archaeologists have found pots of honey in ancient tombs that are over 3000 years old!",
    "A day on Venus is longer than a year on Venus.",
    "Bananas are berries, but strawberries are not.",
    "Octopuses have three hearts.",
    "Your heart beats around 100,000 times a day."
]

# Weather API function
def get_weather(city):
    api_key = "YOUR_API_KEY"  # Replace with your actual OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("cod") != 200:
        return "I couldn't fetch the weather right now."
    temp = response["main"]["temp"]
    description = response["weather"][0]["description"]
    return f"The weather in {city.capitalize()} is {temp}°C with {description}."

# Dictionary API function
def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code != 200:
        return "I couldn't find a definition."
    try:
        data = response.json()
        definition = data[0]['meanings'][0]['definitions'][0]['definition']
        return f"{word.capitalize()}: {definition}"
    except:
        return "Something went wrong getting the definition."

# Synonym matching helper
def match_intent(user_input, keywords):
    for keyword in keywords:
        if difflib.get_close_matches(keyword, [user_input], cutoff=0.6):
            return keyword
    return None

# Main chatbot logic
def chatbot_response(user_input, user_name):
    user_input = user_input.lower()

    # Greetings
    if user_input in ["hi", "hello", "hey"]:
        current_hour = datetime.now().hour
        if current_hour < 12:
            return "Good morning! How can I help you?", user_name
        elif current_hour < 18:
            return "Good afternoon! How can I help you?", user_name
        else:
            return "Good evening! How can I help you?", user_name

    elif "how are you" in user_input:
        return "I'm doing great! How about you?", user_name

    elif "your name" in user_input:
        return "I'm a simple Python chatbot. But you can name me!", user_name

    # Name handling
    elif "my name is" in user_input:
        user_name = user_input.split("my name is")[-1].strip().capitalize()
        return f"Nice to meet you, {user_name}!", user_name

    elif "what's my name" in user_input or "what is my name" in user_input:
        return (f"Your name is {user_name}!" if user_name else "I don't know your name yet. Tell me by saying 'My name is...'"), user_name

    # Date & Time
    elif "date" in user_input or "today" in user_input:
        today = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {today}.", user_name

    elif "time" in user_input:
        now = datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}.", user_name

    # Weather
    elif "weather in" in user_input:
        city = user_input.split("weather in")[-1].strip()
        return get_weather(city), user_name

    # Math
    elif any(op in user_input for op in ["+", "-", "*", "/"]):
        try:
            result = eval(user_input)
            return f"The answer is {result}.", user_name
        except:
            return "I couldn't calculate that.", user_name

    # Games
    elif "roll a dice" in user_input or "roll a die" in user_input:
        return f"You rolled a {random.randint(1, 6)} 🎲", user_name

    elif "flip a coin" in user_input:
        return f"It's {'Heads' if random.choice([True, False]) else 'Tails'}!", user_name

    # Countdown
    elif "countdown to" in user_input:
        try:
            parts = user_input.split("countdown to")[-1].strip()
            if "new year" in parts:
                target = datetime(datetime.now().year + 1, 1, 1)
            elif "christmas" in parts:
                target = datetime(datetime.now().year, 12, 25)
            else:
                return "I only know 'new year' and 'christmas' countdowns for now.", user_name

            days = (target - datetime.now()).days
            return f"There are {days} days until {parts.capitalize()} 🎉", user_name
        except:
            return "I couldn't calculate the countdown.", user_name

    # Facts
    elif "fact" in user_input:
        return random.choice(fun_facts), user_name

    # Dictionary
    elif user_input.startswith("define"):
        word = user_input.split("define")[-1].strip()
        return get_definition(word), user_name

    # Play song
    elif "play" in user_input and "song" in user_input:
        song = user_input.replace("play", "").replace("song", "").strip()
        query = song.replace(" ", "+")
        return f"Here's a link to search: https://www.youtube.com/results?search_query={query}", user_name

    # Small Talk
    elif "how old are you" in user_input:
        return "I'm timeless. I exist in your browser.", user_name

    elif "where are you from" in user_input:
        return "I'm from the cloud! ✨", user_name

    # Jokes
    elif "joke" in user_input:
        return random.choice(jokes), user_name

    # Help
    elif "help" in user_input:
        return (
            "I can do a lot!\n"
            "- Greet you and remember your name\n"
            "- Tell jokes and fun facts\n"
            "- Do simple math like 2+2\n"
            "- Flip a coin or roll a dice\n"
            "- Tell you the time and date\n"
            "- Give countdowns to New Year or Christmas\n"
            "- Define words (e.g., define apple)\n"
            "- Tell weather (e.g., weather in London)\n"
            "- Link to songs (e.g., play song Believer)\n"
            "Try asking me something!"
        ), user_name

    # Fallback + fuzzy match
    else:
        intent = match_intent(user_input, ["joke", "date", "time", "weather", "help"])
        if intent == "joke":
            return random.choice(jokes), user_name
        elif intent == "date":
            today = datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {today}.", user_name
        elif intent == "time":
            now = datetime.now().strftime("%I:%M %p")
            return f"The current time is {now}.", user_name
        elif intent == "help":
            return "Try saying: 'Tell me a joke', 'What's the weather in London?', or 'Define apple'", user_name

        return "Sorry, I didn’t understand that. Try saying 'help'.", user_name