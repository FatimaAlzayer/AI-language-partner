import random
import re

def get_ai_reply(message, language, scenario, character, first_message=False):
    lang = language.lower() if language else "english"
    scen = scenario.lower() if scenario else "restaurant"

    if first_message:
        return get_welcome_message(lang, scen), empty_feedback()

    reply = generate_response(message, lang, scen)
    feedback = generate_feedback(message, lang, scen)

    return reply, feedback


def get_welcome_message(language, scenario):
    welcomes = {
        'english': {
            'restaurant': "Welcome to our restaurant! What would you like to order today?",
            'airport': "Welcome to the airport! Do you need help with your flight?",
            'interview': "Welcome to the interview! Tell me about yourself.",
            'hospital': "Welcome to the hospital! How can I help you today?",
            'default': f"Hi! I'm your {scenario} guide. Ready to practice?"
        },
        'french': {
            'restaurant': "Bienvenue au restaurant! Que souhaitez-vous commander?",
            'airport': "Bienvenue à l'aéroport! Besoin d'aide pour votre vol?",
            'interview': "Bienvenue à l'entretien! Parlez-moi de vous.",
            'hospital': "Bienvenue à l'hôpital! Comment puis-je vous aider?",
            'default': f"Bonjour! Je suis votre guide {scenario}. Prêt à pratiquer?"
        },
        'spanish': {
            'restaurant': "¡Bienvenido al restaurante! ¿Qué desea ordenar?",
            'airport': "¡Bienvenido al aeropuerto! ¿Necesita ayuda con su vuelo?",
            'interview': "¡Bienvenido a la entrevista! Háblame de ti.",
            'hospital': "¡Bienvenido al hospital! ¿Cómo puedo ayudarle?",
            'default': f"¡Hola! Soy tu guía {scenario}. ¿Listo para practicar?"
        },
        'german': {
            'restaurant': "Willkommen im Restaurant! Was möchten Sie bestellen?",
            'airport': "Willkommen am Flughafen! Brauchen Sie Hilfe bei Ihrem Flug?",
            'interview': "Willkommen zum Vorstellungsgespräch! Erzählen Sie mir von sich.",
            'hospital': "Willkommen im Krankenhaus! Wie kann ich Ihnen helfen?",
            'default': f"Hallo! Ich bin Ihr {scenario}-Führer. Bereit zu üben?"
        }
    }

    lang_dict = welcomes.get(language, welcomes['english'])
    return lang_dict.get(scenario, lang_dict['default'])


def generate_response(message, language, scenario):
    message_lower = message.lower()

    # Predefined responses
    responses = {
        'restaurant': {
            'english': ["What would you like to order?", "Would you like to see the menu?"],
            'french': ["Que voulez-vous commander?", "Voulez-vous voir le menu?"],
            'spanish': ["¿Qué le gustaría pedir?", "¿Quiere ver el menú?"],
            'german': ["Was möchten Sie bestellen?", "Möchten Sie die Speisekarte sehen?"]
        },
        'airport': {
            'english': ["Your boarding pass, please.", "Gate 23 is at the end of the hall."],
            'french': ["Votre carte d'embarquement, s'il vous plaît.", "La porte 23 est au bout du couloir."],
            'spanish': ["Su tarjeta de embarque, por favor.", "La puerta 23 está al final del pasillo."],
            'german': ["Ihre Bordkarte, bitte.", "Tor 23 ist am Ende der Halle."]
        },
        # Add other scenarios similarly...
    }

    scenario_dict = responses.get(scenario, responses['restaurant'])
    lang_responses = scenario_dict.get(language, scenario_dict.get('english', []))

    if not lang_responses:
        return "I'm ready to chat!"  # fallback

    return random.choice(lang_responses)


def generate_feedback(message, language, scenario):
    feedback = {'grammar': 'Good', 'suggestion': '', 'new_phrase': ''}
    words = message.split()
    message_lower = message.lower()

    if len(words) < 3:
        feedback['grammar'] = 'Needs improvement'
        feedback['suggestion'] = 'Try using longer, complete sentences.'
    elif message[0].islower():
        feedback['grammar'] = 'Needs improvement'
        feedback['suggestion'] = 'Start your sentence with a capital letter.'

    return feedback


def empty_feedback():
    return {'grammar': '', 'suggestion': '', 'new_phrase': ''}

