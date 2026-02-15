// Get saved language & scenario from index.html selections
const language = localStorage.getItem("language");       
const scenario = localStorage.getItem("scenario");       
const character = localStorage.getItem("character") || "Friend"; 

// DOM elements
const chatBox = document.getElementById("chatBox");
const userMessage = document.getElementById("userMessage");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");  // use existing button

// Add message to chat box
function addMessage(sender, text) {
    const p = document.createElement("p");
    p.innerText = `${sender}: ${text}`;
    chatBox.appendChild(p);
    chatBox.scrollTop = chatBox.scrollHeight; 
}

// Send message to backend
async function sendMessage() {
    const message = userMessage.value.trim();
    if (!message) return;

    addMessage("You", message);

    try {
        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message, language, scenario, character})
        });

        const data = await response.json();

        if (data.error) {
            addMessage("System", data.error);
            return;
        }

        addMessage("AI", data.reply);

        // Voice output
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(data.reply);
            utterance.lang = language.toLowerCase() || "en-US";
            window.speechSynthesis.speak(utterance);
        }

        // Update feedback panel
        document.getElementById("grammar").innerText = data.feedback.grammar;
        document.getElementById("suggestion").innerText = data.feedback.suggestion;
        document.getElementById("newPhrase").innerText = data.feedback.new_phrase;

    } catch (err) {
        console.error(err);
        addMessage("System", "Error connecting to backend.");
    }

    userMessage.value = "";
}

// --- Voice Input ---
let recognition;
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = language.toLowerCase() || "en-US";

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

// Send on button click or Enter key
sendBtn.addEventListener("click", sendMessage);
userMessage.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});
