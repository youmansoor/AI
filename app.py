from flask import Flask, render_template, request, session, jsonify
from chatbot import chatbot_response
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route("/", methods=["GET"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []
    return render_template("index.html", chat_history=session["chat_history"])

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    response, _ = chatbot_response(user_input, None)
    timestamp = datetime.now().strftime("%H:%M:%S")

    session["chat_history"].append({
        "user": user_input,
        "bot": response,
        "timestamp": timestamp
    })
    return jsonify({"user": user_input, "bot": response, "timestamp": timestamp})

if __name__ == "__main__":
    app.run(debug=True)