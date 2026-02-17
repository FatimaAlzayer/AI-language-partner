import random


def get_ai_reply(message, language, scenario, character, first_message=False):
    lang = language.lower() if language else "english"
    scen = scenario.lower() if scenario else "restaurant"

    if first_message:
        return get_welcome_message(lang, scen), empty_feedback()

    reply = generate_response(message, lang, scen)
    feedback = generate_feedback(message, lang, scen)

    return reply, feedback


# -----------------------------------
# WELCOME MESSAGE
# -----------------------------------

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


# -----------------------------------
# RESPONSE GENERATION
# -----------------------------------

def generate_response(message, language, scenario):
    message_lower = message.lower()

    # Goodbye detection
    goodbye_words = ["bye", "goodbye", "thanks", "thank you", "merci", "gracias", "danke"]
    if any(word in message_lower for word in goodbye_words):
        goodbyes = {
            "english": "Goodbye! Great job practicing today 👋",
            "french": "Au revoir! Bon travail aujourd'hui 👋",
            "spanish": "¡Adiós! Buen trabajo practicando 👋",
            "german": "Auf Wiedersehen! Gute Arbeit heute 👋"
        }
        return goodbyes.get(language, goodbyes["english"])

    # Scenario responses
    responses = {
        'restaurant': {
            'english': ["What would you like to order?", "Would you like to see the menu?"],
            'french': ["Que voulez-vous commander?", "Voulez-vous voir le menu?"],
            'spanish': ["¿Qué le gustaría pedir?", "¿Quiere ver el menú?"],
            'german': ["Was möchten Sie bestellen?", "Möchten Sie die Speisekarte sehen?"]
        },
        'airport': {
            'english': ["Your boarding pass, please.", "Which gate are you looking for?"],
            'french': ["Votre carte d'embarquement, s'il vous plaît.", "Quelle porte cherchez-vous?"],
            'spanish': ["Su tarjeta de embarque, por favor.", "¿Qué puerta busca?"],
            'german': ["Ihre Bordkarte, bitte.", "Welches Gate suchen Sie?"]
        },
        'hospital': {
            'english': ["What symptoms are you experiencing?", "How long have you felt this pain?"],
            'french': ["Quels sont vos symptômes?", "Depuis quand avez-vous mal?"],
            'spanish': ["¿Qué síntomas tiene?", "¿Desde cuándo siente dolor?"],
            'german': ["Welche Symptome haben Sie?", "Seit wann haben Sie Schmerzen?"]
        },
        'interview': {
            'english': ["Tell me about yourself.", "What are your strengths?"],
            'french': ["Parlez-moi de vous.", "Quelles sont vos forces?"],
            'spanish': ["Háblame de ti.", "¿Cuáles son tus fortalezas?"],
            'german': ["Erzählen Sie mir von sich.", "Was sind Ihre Stärken?"]
        }
    }

    if scenario not in responses:
        scenario = "restaurant"

    scenario_dict = responses[scenario]
    lang_responses = scenario_dict.get(language, scenario_dict['english'])

    response = random.choice(lang_responses)

    
    while response == message:
     response = random.choice(lang_responses)

    return response



# -----------------------------------
# FEEDBACK GENERATION
# -----------------------------------

def generate_feedback(message, language, scenario):
    feedback = {
        'grammar': 'Good',
        'suggestion': '',
        'new_phrase': ''
    }

    words = message.split()

    # Simple grammar checks
    if len(words) < 3:
        feedback['grammar'] = 'Needs improvement'
        feedback['suggestion'] = 'Try using longer, complete sentences.'
    elif message and message[0].islower():
        feedback['grammar'] = 'Needs improvement'
        feedback['suggestion'] = 'Start your sentence with a capital letter.'

    # Vocabulary suggestions
    vocab = {
        'restaurant': {
            'english': ['I would like to order...', 'Could I see the menu?', 'The bill, please.'],
            'french': ['Je voudrais commander...', 'Puis-je voir le menu?', "L'addition, s'il vous plaît."],
            'spanish': ['Me gustaría pedir...', '¿Puedo ver el menú?', 'La cuenta, por favor.'],
            'german': ['Ich möchte bestellen...', 'Kann ich die Speisekarte sehen?', 'Die Rechnung, bitte.']
        },
        'airport': {
            'english': ['Where is the gate?', 'I have a connecting flight.', 'Where is baggage claim?'],
            'french': ['Où est la porte?', "J'ai un vol de correspondance.", 'Où sont les bagages?'],
            'spanish': ['¿Dónde está la puerta?', 'Tengo un vuelo de conexión.', '¿Dónde está el equipaje?'],
            'german': ['Wo ist das Gate?', 'Ich habe einen Anschlussflug.', 'Wo ist die Gepäckausgabe?']
        },
        'hospital': {
            'english': ['I feel dizzy.', 'I need a doctor.', 'It hurts here.'],
            'french': ['Je me sens étourdi.', "J'ai besoin d'un médecin.", 'Ça fait mal ici.'],
            'spanish': ['Me siento mareado.', 'Necesito un médico.', 'Me duele aquí.'],
            'german': ['Mir ist schwindelig.', 'Ich brauche einen Arzt.', 'Es tut hier weh.']
        },
        'interview': {
            'english': ['I have experience in...', 'I am a quick learner.', 'My strength is teamwork.'],
            'french': ["J'ai de l'expérience en...", 'Je suis motivé.', 'Ma force est le travail en équipe.'],
            'spanish': ['Tengo experiencia en...', 'Aprendo rápido.', 'Mi fortaleza es el trabajo en equipo.'],
            'german': ['Ich habe Erfahrung in...', 'Ich lerne schnell.', 'Meine Stärke ist Teamarbeit.']
        }
    }

    if scenario in vocab:
        vocab_dict = vocab[scenario]
        lang_vocab = vocab_dict.get(language, vocab_dict['english'])
        feedback['new_phrase'] = random.choice(lang_vocab)

    return feedback


def empty_feedback():
    return {
        'grammar': '',
        'suggestion': '',
        'new_phrase': ''
    }
5
