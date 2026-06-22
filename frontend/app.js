const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const chatBox = document.getElementById("chatBox");

const API_URL = "http://127.0.0.1:8000/chat";

// دالة لاكتشاف هل النص يحتوي على حروف عربية لتحديد اتجاه النص
function isArabic(text) {
  const arabicPattern = /[\u0600-\u06FF]/;
  return arabicPattern.test(text);
}

// دالة لتحويل النص العادي إلى HTML منسق (للقوائم، الفقرات، والخط العريض)
function formatResponse(text) {
  // 1. تحويل الروابط المكتوبة بصيغة Markdown [اسم الموقع](الرابط)
  let html = text.replace(/\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)/g, '<a href="$2" target="_blank" style="color: #10B981; font-weight: bold; text-decoration: underline;">$1</a>');
  
  // 2. تحويل الروابط العادية المباشرة
  html = html.replace(/(^|[^\w"'])(https?:\/\/[^\s\)]+)/g, '$1<a href="$2" target="_blank" style="color: #10B981; font-weight: bold; text-decoration: underline;">$2</a>');
  
  // 3. تنسيق الخط العريض والقوائم والأسطر
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\n-/g, '<br>•');
  html = html.replace(/\n/g, '<br>');
  
  return html;
}

// دالة لإضافة الرسائل إلى واجهة المحادثة
function addMessage(text, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message");
  messageDiv.classList.add(sender === "user" ? "user-message" : "bot-message");
  
  // تحديد اتجاه النص بناءً على اللغة
  const textDirection = isArabic(text) ? "rtl" : "ltr";
  messageDiv.setAttribute("dir", textDirection);

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

// دالة لإظهار مؤشر التحميل (Typing indicator)
function addLoadingIndicator() {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", "bot-message");
  messageDiv.setAttribute("id", "loadingMsg");
  
  const avatar = document.createElement("div");
  avatar.classList.add("avatar");
  avatar.textContent = "🎓";

  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  bubble.innerHTML = `
    <div class="typing-indicator">
      <span></span><span></span><span></span>
    </div>
  `;

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(bubble);
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// دالة لإزالة مؤشر التحميل
function removeLoadingIndicator() {
  const loadingMsg = document.getElementById("loadingMsg");
  if (loadingMsg) {
    loadingMsg.remove();
  }
}

// معالجة إرسال النموذج (الدردشة)
chatForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const message = userInput.value.trim();
  if (!message) return;

  // 1. إضافة رسالة المستخدم
  addMessage(message, "user");
  userInput.value = "";

  // 2. إضافة مؤشر التحميل
  addLoadingIndicator();

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    removeLoadingIndicator();
    
    // 3. إضافة رسالة الذكاء الاصطناعي مع معالجة احترافية للأخطاء
    if (response.ok && data.reply) {
        addMessage(data.reply, "bot");
    } else {
        addMessage(`عذراً، خطأ في السيرفر: ${data.detail || 'يرجى التحقق من المفتاح أو إعدادات السيرفر.'}`, "bot");
    }

  } catch (error) {
    removeLoadingIndicator();
    addMessage("عذراً، لا يمكن الاتصال بالسيرفر. تأكد من تشغيل الـ Backend.", "bot");
  }
});

// --- تفعيل الأزرار الجانبية (Smart Services) كأوامر سريعة ---
const menuButtons = document.querySelectorAll('.menu-btn[data-prompt]');

menuButtons.forEach(button => {
  button.addEventListener('click', () => {
    // 1. تغيير التصميم ليوضح أي زر هو النشط حالياً
    document.querySelectorAll('.menu-btn').forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');

    // 2. جلب السؤال المخبأ داخل الزر
    const promptText = button.getAttribute('data-prompt');

    // 3. وضع السؤال في مربع النص وإرساله تلقائياً
    userInput.value = promptText;
    chatForm.dispatchEvent(new Event('submit'));
  });
});

// إعادة تفعيل زر المحادثة الأساسي (AI Chat Consultant)
const chatBtn = document.querySelector('.menu-btn:not([data-prompt])');
if(chatBtn) {
    chatBtn.addEventListener('click', () => {
        document.querySelectorAll('.menu-btn').forEach(btn => btn.classList.remove('active'));
        chatBtn.classList.add('active');
        userInput.focus();
    });
}