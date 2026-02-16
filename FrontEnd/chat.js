function sendMessage() {
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  if (input.value.trim() === "") return;

  const userMessage = document.createElement("div");
  userMessage.textContent = "You: " + input.value;
  chatBox.appendChild(userMessage);

  // رد تجريبي من AI
  const aiMessage = document.createElement("div");
  aiMessage.textContent = "AI: Hello 👋";
  chatBox.appendChild(aiMessage);

  input.value = "";
  chatBox.scrollTop = chatBox.scrollHeight;
}
