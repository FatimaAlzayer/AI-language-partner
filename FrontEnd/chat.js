const chatBox = document.getElementById("chatBox");

function addMessage(text, sender){
    const msg = document.createElement("div");
    msg.classList.add("message", sender);
    msg.innerText = text;
    chatBox.appendChild(msg);

    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(){

    const input = document.getElementById("messageInput");
    const message = input.value.trim();

    if(message === "") return;

    addMessage(message, "user");
    input.value = "";

    try{
        const response = await fetch("http://127.0.0.1:5000/chat",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        addMessage(data.reply, "ai");

    }catch(error){
        addMessage("Error connecting to server", "ai");
        console.error(error);
    }
}
