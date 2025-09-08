# app.py
from flask import Flask, render_template, request, jsonify, session
from chatbot import chatbot_response
from datetime import datetime
import os

# Tell Flask to look for templates in current directory (root)
app = Flask(__name__, template_folder='.')
app.secret_key = os.urandom(24)  # Needed for sessions

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

    bot_reply, session_user_name = chatbot_response(user_message, session.get("user_name"))
    if session_user_name:
        session["user_name"] = session_user_name

    timestamp = datetime.now().strftime("%H:%M:%S")
    session["chat_history"].append({"user": user_message, "bot": bot_reply, "timestamp": timestamp})
    session.modified = True

    return jsonify({
        "user": user_message,
        "bot": bot_reply,
        "timestamp": timestamp
    })

if __name__ == "__main__":
    app.run(debug=True)