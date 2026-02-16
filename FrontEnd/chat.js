// Get saved language & scenario from index.html selections
const language = localStorage.getItem("language")?.toLowerCase() || "english";       
const scenario = localStorage.getItem("scenario")?.toLowerCase() || "restaurant";       
const character = localStorage.getItem("character") || "Friend"; 

const chatBox = document.getElementById("chatBox");
const userMessage = document.getElementById("userMessage");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");

function addMessage(text, sender){
    const msg = document.createElement("div");
    msg.classList.add("message", sender);
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight; 
}

async function sendMessage(){
    const message = userMessage.value.trim();
    if (!message) return;

    addMessage(message, "user");
    userMessage.value = "";

    try {
        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ message, language, scenario, character })
        });

        const data = await response.json();

        if (data.error) {
            addMessage(data.error, "ai");
            return;
        }

        addMessage(data.reply, "ai");

        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(data.reply);
            utterance.lang = language === 'english' ? 'en-US' :
                             language === 'french' ? 'fr-FR' :
                             language === 'spanish' ? 'es-ES' :
                             language === 'german' ? 'de-DE' : 'en-US';
            window.speechSynthesis.speak(utterance);
        }

        document.getElementById("grammar").innerText = data.feedback.grammar || '-';
        document.getElementById("suggestion").innerText = data.feedback.suggestion || '-';
        document.getElementById("newPhrase").innerText = data.feedback.new_phrase || '-';

    } catch (err) {
        addMessage("Error connecting to backend.", "ai");
        console.error(err);
    }
}

// Voice input
let recognition;
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = language === 'english' ? 'en-US' :
                      language === 'french' ? 'fr-FR' :
                      language === 'spanish' ? 'es-ES' :
                      language === 'german' ? 'de-DE' : 'en-US';

    micBtn.addEventListener("click", () => recognition.start());

    recognition.onresult = (event) => {
        const speech = event.results[0][0].transcript;
        userMessage.value = speech;
        sendMessage();
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error", event.error);
    };
} else {
    micBtn.disabled = true;
    micBtn.title = "Voice input not supported";
}

// Send on click or Enter
sendBtn.addEventListener("click", sendMessage);
userMessage.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});


