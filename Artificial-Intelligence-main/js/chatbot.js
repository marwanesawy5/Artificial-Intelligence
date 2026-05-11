document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chatBox");
  const input = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");
  const saveBtn = document.getElementById("saveBtn");
  const quickButtons = document.querySelectorAll(".ask-btn");

  /* ========================
     Create Message Bubble
  ======================== */
  function createMessage(text, type = "bot") {

    const wrapper = document.createElement("div");
    wrapper.classList.add("message");

    if (type === "user") {
      wrapper.classList.add("user-msg");
    } else {
      wrapper.classList.add("bot-msg");
    }

    const avatar = document.createElement("div");
    avatar.classList.add("avatar");
    avatar.textContent = type === "user" ? "🧑" : "🤖";

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.innerHTML = text;

    if (type === "user") {
      wrapper.appendChild(bubble);
      wrapper.appendChild(avatar);
    } else {
      wrapper.appendChild(avatar);
      wrapper.appendChild(bubble);
    }

    chatBox.appendChild(wrapper);
    scrollBottom();
  }

  /* ========================
     Auto Scroll
  ======================== */
  function scrollBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  /* ========================
     Typing Loader
  ======================== */
  function typingLoader() {

    const typing = document.createElement("div");
    typing.classList.add("message", "bot-msg");
    typing.id = "typingBox";

    typing.innerHTML = `
      <div class="avatar">🤖</div>
      <div class="bubble">Typing...</div>
    `;

    chatBox.appendChild(typing);
    scrollBottom();
  }

  function removeTyping() {
    const typing = document.getElementById("typingBox");
    if (typing) typing.remove();
  }

  /* ========================
     Save Conversation
  ======================== */
  function saveConversation() {

    const messages = document.querySelectorAll(".message");
    let text = "FinAI Chat Conversation\n";
    text += "=========================\n\n";

    messages.forEach(msg => {

      const bubble = msg.querySelector(".bubble");
      if (!bubble) return;

      const isUser = msg.classList.contains("user-msg");

      text += isUser ? "You: " : "FinAI: ";
      text += bubble.innerText + "\n\n";

    });

    const blob = new Blob([text], { type: "text/plain" });
    const link = document.createElement("a");

    link.href = URL.createObjectURL(blob);
    link.download = "FinAI_Conversation.txt";
    link.click();

    URL.revokeObjectURL(link.href);
  }

  /* ========================
     Send Message to AI
  ======================== */
  async function sendMessage() {

    const text = input.value.trim();

    if (text === "") return;

    createMessage(text, "user");
    input.value = "";
    input.focus();

    typingLoader();

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: text
        })
      });

      const data = await response.json();
      removeTyping();

      if (data.reply) {
        createMessage(data.reply, "bot");
      } else {
        createMessage("No response received.", "bot");
      }

    } catch (error) {

      removeTyping();
      createMessage("Server error. Please try again.", "bot");

    }
  }

  /* ========================
     Events
  ======================== */

  if (sendBtn) {
    sendBtn.addEventListener("click", sendMessage);
  }

  if (saveBtn) {
    saveBtn.addEventListener("click", saveConversation);
  }

  if (input) {
    input.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
      }
    });
  }

  /* ========================
     Quick Buttons
  ======================== */
  quickButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      input.value = btn.textContent;
      sendMessage();
    });
  });
});