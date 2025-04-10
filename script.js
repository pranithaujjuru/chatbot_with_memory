const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");

function appendMessage(msg, type) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add(type);
  msgDiv.textContent = msg;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const message = input.value.trim();
  if (!message) return;

  appendMessage(message, "user");
  input.value = "";

  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  const data = await res.json();
  appendMessage(data.response, "bot");
}

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});
