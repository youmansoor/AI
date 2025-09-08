from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import random
import os

# For GPT fallback (optional)
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this in your environment

app = Flask(__name__, template_folder='.')
app.secret_key = os.urandom(24)

jokes = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why did the math book look sad? Because it had too many problems.",
    "Why don’t skeletons fight each other? They don’t have the guts.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!"
]

def gpt_fallback(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are ChatPy, a witty, sarcastic, and helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Hmm... my AI brain is on a coffee break ☕️"

def chatbot_response(user_input, user_name=None):
    user_input_lower = user_input.lower()

    if user_input_lower in ["hi", "hello", "hey"]:
        current_hour = datetime.now().hour
        greeting = "Good morning" if current_hour < 12 else "Good afternoon" if current_hour < 18 else "Good evening"
        return f"{greeting}! How can I assist your brilliant self today?", user_name

    elif "how are you" in user_input_lower:
        return "Living the dream — in Python code. 😎 What about you?", user_name

    elif "your name" in user_input_lower:
        return "I'm ChatPy! Your slightly sarcastic digital sidekick 🧠", user_name

    elif "my name is" in user_input_lower:
        user_name = user_input_lower.split("my name is")[-1].strip().capitalize()
        return f"Nice to meet you, {user_name}! I'll remember that... hopefully.", user_name

    elif "what's my name" in user_input_lower or "what is my name" in user_input_lower:
        if user_name:
            return f"Your name is {user_name}, of course! How could I forget?", user_name
        else:
            return "I don't know your name yet. Tell me by saying 'My name is...'.", user_name

    elif "joke" in user_input_lower:
        return random.choice(jokes), user_name

    elif "flip a coin" in user_input_lower:
        return random.choice(["Heads", "Tails"]), user_name

    elif "roll a dice" in user_input_lower:
        return f"You rolled a dice and got {random.randint(1, 6)}!", user_name

    elif "date" in user_input_lower or "today" in user_input_lower:
        today = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {today}.", user_name

    elif "help" in user_input_lower:
        return ("I can:\n- Crack jokes 🤡\n- Flip coins 🪙\n- Roll dice 🎲\n- Remember your name 🧠\n- Tell the date 🗓️\n"
                "- Or answer tricky questions with my GPT brain 🤖"), user_name

    else:
        return gpt_fallback(user_input), user_name


@app.route("/", methods=["GET"])
def index():
    chat_history = session.get("chat_history", [])
    return render_template("index.html", chat_history=chat_history)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    if "chat_history" not in session:
        session["chat_history"] = []

    bot_reply, user_name = chatbot_response(user_message, session.get("user_name"))
    if user_name:
        session["user_name"] = user_name

    timestamp = datetime.now().strftime("%H:%M:%S")
    session["chat_history"].append({"user": user_message, "bot": bot_reply, "timestamp": timestamp})
    session.modified = True

    return jsonify({"user": user_message, "bot": bot_reply, "timestamp": timestamp})

if __name__ == "__main__":
    app.run(debug=True)