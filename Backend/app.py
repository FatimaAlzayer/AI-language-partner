from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_logic import get_ai_reply

app = Flask(__name__)
CORS(app)  # allows frontend to talk to backend

# Keep track if first message per session
first_message_flag = {}

@app.route("/")
def home():
    return "Welcome to the AI Language Partner API!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    session_id = data.get("session_id", "default")  # optional session identifier
    message = data.get("message")
    language = data.get("language")
    scenario = data.get("scenario")
    character = data.get("character", "Friend")  # default

    if not message or not language or not scenario:
        return jsonify({"error": "Missing fields"}), 400

    # Determine if this is the first message for this session
    first_message = not first_message_flag.get(session_id, False)

    # Get AI reply and feedback
    reply, feedback = get_ai_reply(message, scenario, character, first_message)

    # Mark that session has received first message
    first_message_flag[session_id] = True

    return jsonify({
        "reply": reply,
        "feedback": feedback
    })

if __name__ == "__main__":
    app.run(debug=True)

    app.run(debug=True)
