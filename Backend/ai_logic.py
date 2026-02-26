import os
from groq import Groq
from dotenv import load_dotenv

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found. Set it in your .env file.")

# -------------------------------
# Initialize Groq client
# -------------------------------
client = Groq(api_key=GROQ_API_KEY)

# -------------------------------
# Conversation memory
# -------------------------------
conversation_history = {}

# -------------------------------
# AI Reply function
# -------------------------------
def get_ai_reply(message, language, scenario, character, first_message=False, session_id="default"):
    if session_id not in conversation_history:
        conversation_history[session_id] = []

    try:
        system_prompt = create_system_prompt(language, scenario, character, first_message)
        messages = [{"role": "system", "content": system_prompt}]

        # Add last 5 messages for context
        messages.extend(conversation_history[session_id][-5:])

        user_content = message if not first_message else "Start the conversation"
        messages.append({"role": "user", "content": user_content})

        # Call Groq API
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=150,
            top_p=0.9,
            stream=False
        )

        reply = response.choices[0].message.content

        # Store conversation
        conversation_history[session_id].append({"role": "user", "content": user_content})
        conversation_history[session_id].append({"role": "assistant", "content": reply})

        feedback = generate_feedback(message, reply, language)
        return reply, feedback

    except Exception as e:
        print(f"Groq API Error: {e}")
        return fallback_response(message, language, scenario, first_message)

# -------------------------------
# System prompt creation
# -------------------------------
def create_system_prompt(language, scenario, character, first_message):
    language_map = {"English": "English", "Spanish": "Spanish", "French": "French", "German": "German"}
    lang = language_map.get(language, "English")

    scenario_descriptions = {
        "Restaurant": "You are a waiter/waitress in a restaurant. Help the customer order food.",
        "Airport": "You are an airport staff member. Help passengers with flight info.",
        "Interview": "You are an HR manager conducting a job interview.",
        "Hospital": "You are a doctor. Ask about symptoms and provide advice."
    }

    base_prompt = f"""You are an AI language partner helping someone practice {lang}.
Current scenario: {scenario_descriptions.get(scenario, scenario_descriptions['Restaurant'])}

CRITICAL RULES FOR VOICE CHAT:
1. Respond ONLY in {lang}
2. KEEP RESPONSES SHORT - 1-3 sentences
3. Be conversational and encouraging
4. Stay in character
5. Use simple vocabulary
"""

    if first_message:
        base_prompt += "\nThis is the first message. Greet warmly in 1-2 sentences."

    return base_prompt

# -------------------------------
# Feedback generator
# -------------------------------
def generate_feedback(user_message, ai_reply, language):
    words = user_message.split()
    feedback = {'grammar': 'Good', 'suggestion': '', 'new_phrase': ''}

    if len(words) < 3:
        feedback['grammar'] = 'Needs improvement'
        feedback['suggestion'] = 'Try using longer sentences.'
    elif user_message and user_message[0].islower() and len(user_message) > 1:
        feedback['grammar'] = 'Needs improvement'
        feedback['suggestion'] = 'Start with a capital letter.'
    elif language == 'English' and ' i ' in f" {user_message.lower()} " and ' I ' not in f" {user_message} ":
        feedback['grammar'] = 'Needs improvement'
        feedback['suggestion'] = "Use capital 'I'."
    elif '?' in user_message:
        feedback['grammar'] = 'Excellent'
        feedback['suggestion'] = 'Great question!'
    else:
        vocab = {
            'English': ['excellent', 'wonderful', 'interesting', 'fascinating'],
            'Spanish': ['excelente', 'maravilloso', 'interesante', 'fascinante'],
            'French': ['excellent', 'merveilleux', 'intéressant', 'fascinant'],
            'German': ['ausgezeichnet', 'wunderbar', 'interessant', 'faszinierend']
        }
        suggestions = vocab.get(language, vocab['English'])
        feedback['new_phrase'] = suggestions[len(words) % len(suggestions)]
        feedback['suggestion'] = 'Keep up the good work!'

    return feedback

# -------------------------------
# Fallback response
# -------------------------------
def fallback_response(message, language, scenario, first_message):
    if first_message:
        welcomes = {
            'English': f"Hi! I'm your {scenario} guide. Ready to practice?",
            'French': f"Bonjour! Je suis votre guide {scenario}. Prêt à pratiquer?",
            'Spanish': f"¡Hola! Soy tu guía {scenario}. ¿Listo para practicar?",
            'German': f"Hallo! Ich bin Ihr {scenario}-Führer. Bereit zu üben?"
        }
        return welcomes.get(language, welcomes['English']), {'grammar':'','suggestion':'','new_phrase':''}

    responses = {
        'Restaurant': {
            'English': "What would you like to order?",
            'French': "Que voulez-vous commander?",
            'Spanish': "¿Qué le gustaría pedir?",
            'German': "Was möchten Sie bestellen?"
        },
        'Airport': {
            'English': "Your boarding pass, please.",
            'French': "Votre carte d'embarquement, s'il vous plaît.",
            'Spanish': "Su tarjeta de embarque, por favor.",
            'German': "Ihre Bordkarte, bitte."
        },
        'Interview': {
            'English': "Tell me about your experience.",
            'French': "Parlez-moi de votre expérience?",
            'Spanish': "Háblame de tu experiencia.",
            'German': "Erzählen Sie mir von Ihrer Erfahrung."
        },
        'Hospital': {
            'English': "What symptoms are you experiencing?",
            'French': "Quels sont vos symptômes?",
            'Spanish': "¿Qué síntomas tiene?",
            'German': "Welche Symptome haben Sie?"
        }
    }

    reply = responses.get(scenario, {}).get(language, responses['Restaurant']['English'])

    return reply, {'grammar': 'Good', 'suggestion': 'Keep practicing!', 'new_phrase': 'good job'}
