import random
import re

def get_ai_reply(message, language, scenario, character, first_message=False):
    
    # Convert to lowercase
    lang = language.lower() if language else "english"
    scen = scenario.lower() if scenario else "restaurant"
    
    #welcome message 
    if first_message:
        return get_welcome_message(lang, scen), empty_feedback()
    
    #generate AI response
    reply = generate_response(message, lang, scen)
    
    #feedback
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
    
    # Get language dictionary, default to English
    lang_dict = welcomes.get(language, welcomes['english'])
    
    # Get scenario message, default to default message
    return lang_dict.get(scenario, lang_dict['default'])


def generate_response(message, language, scenario):
    """Generate AI response based on user message"""
    
    message_lower = message.lower()
    
    #set of possible responses for each scenario and language
    responses = {
        'restaurant': {
            'english': [
                "What would you like to order?",
                "Would you like to see the menu?",
                "Our special today is pasta.",
                "Can I get you something to drink?",
                "How would you like your steak cooked?",
                "Would you like appetizers?",
                "The soup of the day is tomato.",
                "Is that for here or to go?"
            ],
            'french': [
                "Que voulez-vous commander?",
                "Voulez-vous voir le menu?",
                "Notre spécial aujourd'hui est les pâtes.",
                "Puis-je vous offrir une boisson?"
            ],
            'spanish': [
                "¿Qué le gustaría pedir?",
                "¿Quiere ver el menú?",
                "Nuestro especial de hoy es pasta.",
                "¿Le puedo ofrecer una bebida?"
            ],
            'german': [
                "Was möchten Sie bestellen?",
                "Möchten Sie die Speisekarte sehen?",
                "Unser heutiges Special ist Pasta.",
                "Kann ich Ihnen etwas zu trinken bringen?"
            ]
        },
        'airport': {
            'english': [
                "Your boarding pass, please.",
                "Gate 23 is at the end of the hall.",
                "Please remove your laptop from the bag.",
                "The flight is on time.",
                "Do you have any checked luggage?",
                "Here is your boarding pass.",
                "The security check is this way.",
                "Please proceed to gate 15."
            ],
            'french': [
                "Votre carte d'embarquement, s'il vous plaît.",
                "La porte 23 est au bout du couloir.",
                "Veuillez retirer votre ordinateur du sac."
            ],
            'spanish': [
                "Su tarjeta de embarque, por favor.",
                "La puerta 23 está al final del pasillo.",
                "Por favor, saque su computadora de la bolsa."
            ],
            'german': [
                "Ihre Bordkarte, bitte.",
                "Tor 23 ist am Ende der Halle.",
                "Bitte nehmen Sie Ihren Laptop aus der Tasche."
            ]
        },
        'interview': {
            'english': [
                "Tell me about your experience.",
                "What are your strengths?",
                "Why do you want this job?",
                "Where do you see yourself in 5 years?",
                "What's your biggest achievement?",
                "Why should we hire you?",
                "Tell me about a challenge you faced.",
                "What are your salary expectations?"
            ],
            'french': [
                "Parlez-moi de votre expérience.",
                "Quelles sont vos forces?",
                "Pourquoi voulez-vous ce poste?"
            ],
            'spanish': [
                "Háblame de tu experiencia.",
                "¿Cuáles son tus fortalezas?",
                "¿Por qué quieres este trabajo?"
            ],
            'german': [
                "Erzählen Sie mir von Ihrer Erfahrung.",
                "Was sind Ihre Stärken?",
                "Warum möchten Sie diese Stelle?"
            ]
        },
        'hospital': {
            'english': [
                "What symptoms are you experiencing?",
                "Take this prescription to the pharmacy.",
                "You need to rest for a few days.",
                "When did the pain start?",
                "Do you have any allergies?",
                "I'll write you a prescription.",
                "Drink plenty of water.",
                "Come back in two weeks for a check-up."
            ],
            'french': [
                "Quels sont vos symptômes?",
                "Apportez cette ordonnance à la pharmacie.",
                "Vous devez vous reposer quelques jours."
            ],
            'spanish': [
                "¿Qué síntomas tiene?",
                "Lleve esta receta a la farmacia.",
                "Necesita descansar unos días."
            ],
            'german': [
                "Welche Symptome haben Sie?",
                "Bringen Sie dieses Rezept in die Apotheke.",
                "Sie müssen sich ein paar Tage ausruhen."
            ]
        }
    }
    
    # Check for greetings
    greetings = ['hello', 'hi', 'hey', 'bonjour', 'hola', 'hallo']
    if any(greeting in message_lower for greeting in greetings):
        return f"Hello! How can I help you at the {scenario} today?"
    
    # Check for questions
    if '?' in message:
        questions = {
            'restaurant': "That's a good question about the menu!",
            'airport': "Good question about your flight!",
            'interview': "Great question during the interview!",
            'hospital': "I understand your concern about your health."
        }
        return questions.get(scenario, "That's a good question!")
    
    # Check for thanks
    thanks = ['thank', 'thanks', 'merci', 'gracias', 'danke']
    if any(word in message_lower for word in thanks):
        thanks_responses = {
            'english': "You're welcome! Is there anything else?",
            'french': "De rien! Autre chose?",
            'spanish': "¡De nada! ¿Algo más?",
            'german': "Gern geschehen! Noch etwas?"
        }
        return thanks_responses.get(language, thanks_responses['english'])
    
    # Check for goodbyes
    goodbyes = ['bye', 'goodbye', 'au revoir', 'adiós', 'auf wiedersehen']
    if any(word in message_lower for word in goodbyes):
        goodbyes_responses = {
            'english': "Goodbye! Come back to practice again!",
            'french': "Au revoir! Revenez pratiquer!",
            'spanish': "¡Adiós! ¡Vuelve a practicar!",
            'german': "Auf Wiedersehen! Kommen Sie wieder zum Üben!"
        }
        return goodbyes_responses.get(language, goodbyes_responses['english'])
    
    # Short message response
    if len(message.split()) < 3:
        short_responses = {
            'english': "Can you tell me more about that?",
            'french': "Pouvez-vous m'en dire plus?",
            'spanish': "¿Puedes contarme más?",
            'german': "Können Sie mir mehr darüber erzählen?"
        }
        return short_responses.get(language, short_responses['english'])
    
    # Get scenario-specific response
    scenario_dict = responses.get(scenario, responses['restaurant'])
    lang_responses = scenario_dict.get(language, scenario_dict.get('english', responses['restaurant']['english']))
    
    return random.choice(lang_responses)


def generate_feedback(message, language, scenario):
    """Generate grammar feedback and suggestions"""
    
    words = message.split()
    message_lower = message.lower()
    
    # Initialize feedback
    feedback = {
        'grammar': 'Good',
        'suggestion': '',
        'new_phrase': ''
    }
    
    
    # Check message length
    if len(words) < 3:
        feedback['grammar'] = 'Needs improvement'
        feedback['suggestion'] = 'Try using longer, complete sentences.'
    
    # Check for capitalization
    elif message[0].islower() and len(message) > 1:
        feedback['grammar'] = 'Needs improvement'
        feedback['suggestion'] = 'Start your sentence with a capital letter.'
    
    # Check for 'i' vs 'I'
    elif ' i ' in f" {message_lower} " and ' I ' not in f" {message} ":
        feedback['grammar'] = 'Needs improvement'
        feedback['suggestion'] = "Use capital 'I' when referring to yourself."
    
    # Check for question marks
    elif '?' in message:
        feedback['grammar'] = 'Excellent'
        feedback['suggestion'] = 'Great question! Keep asking.'
    
    # Check for exclamation marks
    elif '!' in message:
        feedback['grammar'] = 'Good'
        feedback['suggestion'] = 'Good enthusiasm!'
    
    # Check for common grammar issues by language
    elif language == 'english':
        # Check for missing articles
        if re.search(r'\b(a|an)\s+[aeiou]', message_lower):
            feedback['grammar'] = 'Good'
            feedback['suggestion'] = "Remember: use 'an' before vowel sounds."
        
        # Check for subject-verb agreement
        if re.search(r'\b(he|she|it) (are|were)\b', message_lower):
            feedback['grammar'] = 'Needs improvement'
            feedback['suggestion'] = "Use 'is' with he/she/it, not 'are'."
        
        elif re.search(r'\b(I|you|we|they) (is|was)\b', message_lower):
            feedback['grammar'] = 'Needs improvement'
            feedback['suggestion'] = "Use 'am/are' with I/you/we/they, not 'is'."
    
    elif language == 'french':
        if re.search(r'\b(je) (est|sont)\b', message_lower):
            feedback['grammar'] = 'Needs improvement'
            feedback['suggestion'] = "Use 'suis' with Je, not 'est' or 'sont'."
    
    elif language == 'spanish':
        if re.search(r'\b(yo) (es|son)\b', message_lower):
            feedback['grammar'] = 'Needs improvement'
            feedback['suggestion'] = "Use 'soy' with Yo, not 'es' or 'son'."
    
    elif language == 'german':
        if re.search(r'\b(ich) (ist|sind)\b', message_lower):
            feedback['grammar'] = 'Needs improvement'
            feedback['suggestion'] = "Use 'bin' with Ich, not 'ist' or 'sind'."
    
    
    #vocabulary suggestions based on scenario and language
    vocab = {
        'restaurant': {
            'english': ['menu', 'appetizer', 'main course', 'dessert', 'waiter'],
            'french': ['menu', 'entrée', 'plat principal', 'dessert', 'serveur'],
            'spanish': ['menú', 'entrante', 'plato principal', 'postre', 'camarero'],
            'german': ['Speisekarte', 'Vorspeise', 'Hauptgericht', 'Nachtisch', 'Kellner']
        },
        'airport': {
            'english': ['boarding pass', 'gate', 'departure', 'arrival', 'luggage'],
            'french': ["carte d'embarquement", 'porte', 'départ', 'arrivée', 'bagages'],
            'spanish': ['tarjeta de embarque', 'puerta', 'salida', 'llegada', 'equipaje'],
            'german': ['Bordkarte', 'Tor', 'Abflug', 'Ankunft', 'Gepäck']
        },
        'interview': {
            'english': ['experience', 'skills', 'position', 'company', 'team'],
            'french': ['expérience', 'compétences', 'poste', 'entreprise', 'équipe'],
            'spanish': ['experiencia', 'habilidades', 'puesto', 'empresa', 'equipo'],
            'german': ['Erfahrung', 'Fähigkeiten', 'Position', 'Firma', 'Team']
        },
        'hospital': {
            'english': ['symptoms', 'prescription', 'doctor', 'medicine', 'appointment'],
            'french': ['symptômes', 'ordonnance', 'médecin', 'médicament', 'rendez-vous'],
            'spanish': ['síntomas', 'receta', 'médico', 'medicina', 'cita'],
            'german': ['Symptome', 'Rezept', 'Arzt', 'Medizin', 'Termin']
        }
    }
    
    # Add vocabulary suggestion if message is good
    if feedback['grammar'] != 'Needs improvement' and len(words) > 3:
        vocab_dict = vocab.get(scenario, vocab['restaurant'])
        lang_vocab = vocab_dict.get(language, vocab_dict['english'])
        feedback['new_phrase'] = random.choice(lang_vocab)
    
    # Add suggestion for improvement
    if feedback['grammar'] == 'Good' and not feedback['suggestion']:
        encouragements = {
            'english': "Great job! Keep practicing.",
            'french': "Bon travail! Continuez à pratiquer.",
            'spanish': "¡Buen trabajo! Sigue practicando.",
            'german': "Gute Arbeit! Üben Sie weiter."
        }
        feedback['suggestion'] = encouragements.get(language, encouragements['english'])
    
    return feedback


def empty_feedback():
    """Return empty feedback for welcome message"""
    return {
        'grammar': '',
        'suggestion': '',
        'new_phrase': ''
    }
