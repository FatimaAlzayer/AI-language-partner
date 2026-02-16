from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_logic import get_ai_reply

app = Flask(__name__)
CORS(app)  # frontend can talk to backend

first_message_flag = {}  # track first message per session

@app.route("/")
def home():
    return "Welcome to the AI Language Partner API!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = data.get("session_id", "default")
    message = data.get("message")
    language = (data.get("language") or "english").lower()
    scenario = (data.get("scenario") or "restaurant").lower()
    character = data.get("character") or "Friend"

    if not message or not language or not scenario:
        return jsonify({"error": "Missing fields"}), 400

    first_message = not first_message_flag.get(session_id, False)

    reply, feedback = get_ai_reply(message, language, scenario, character, first_message)

    first_message_flag[session_id] = True

    return jsonify({
        "reply": reply,
        "feedback": feedback
    })

if __name__ == "__main__":
    app.run(debug=True)
