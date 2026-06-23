const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const chatBox = document.getElementById("chatBox");

// إذا قمت برفع الخلفية على Render، ضع الرابط هنا. حالياً هو يعمل على جهازك.
const API_URL = "http://127.0.0.1:8000/chat";

function isArabic(text) {
  return /[\u0600-\u06FF]/.test(text);
}

function formatResponse(text) {
  let html = text.replace(/\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
  html = html.replace(/(^|[^\w"'])(https?:\/\/[^\s\)]+)/g, '$1<a href="$2" target="_blank">$2</a>');
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\n-/g, '<br>•');
  html = html.replace(/\n/g, '<br>');
  return html;
}

function addMessage(text, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");
  messageDiv.setAttribute("dir", isArabic(text) ? "rtl" : "ltr");

  const avatar = document.createElement("div");
  avatar.classList.add("avatar");
  avatar.textContent = sender === "user" ? "👤" : "🎓";

  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  
  if(sender === "bot") {
      bubble.innerHTML = formatResponse(text);
  } else {
      bubble.textContent = text;
  }

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(bubble);
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
  return bubble;
}

function addLoadingIndicator() {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", "bot-message");
  messageDiv.setAttribute("id", "loadingMsg");
  messageDiv.innerHTML = `<div class="avatar">🎓</div><div class="bubble"><div class="typing-indicator"><span></span><span></span><span></span></div></div>`;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

chatForm.addEventListener("submit", async function (event) {
  event.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;

  addMessage(message, "user");
  userInput.value = "";
  addLoadingIndicator();

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });
    const data = await response.json();
    document.getElementById("loadingMsg")?.remove();
    
    if (response.ok && data.reply) {
        addMessage(data.reply, "bot");
    } else {
        addMessage(`عذراً، خطأ تقني: ${data.detail || 'تأكد من المفتاح'}`, "bot");
    }
  } catch (error) {
    document.getElementById("loadingMsg")?.remove();
    addMessage("عذراً، لا يمكن الاتصال بالسيرفر. تأكد من تشغيل الـ Backend.", "bot");
  }
});

const menuButtons = document.querySelectorAll('.menu-btn[data-prompt]');
menuButtons.forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.menu-btn').forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
    userInput.value = button.getAttribute('data-prompt');
    chatForm.dispatchEvent(new Event('submit'));
  });
});

const chatBtn = document.querySelector('.menu-btn:not([data-prompt])');
if(chatBtn) {
    chatBtn.addEventListener('click', () => {
        document.querySelectorAll('.menu-btn').forEach(btn => btn.classList.remove('active'));
        chatBtn.classList.add('active');
        userInput.focus();
    });
}