const chat = document.getElementById("chat");
const form = document.getElementById("form");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const sendLabel = document.getElementById("send-label");
const statusEl = document.getElementById("status");
const passwordInput = document.getElementById("password");
const statDocs = document.getElementById("stat-docs");
const statModel = document.getElementById("stat-model");

const API_BASE = "";

const INTENT_LABELS = {
  question: "Business Q&A",
  lead_prep: "Strategy Session Prep",
};

function createAvatar(role) {
  const av = document.createElement("div");
  av.className = `avatar avatar-${role}`;
  av.innerHTML = role === "bot" ? "<span>CC</span>" : "<span>You</span>";
  return av;
}

function formatText(text) {
  const escaped = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
  return escaped
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n\n/g, "</p><p>")
    .replace(/\n/g, "<br>");
}

function addMessage(text, role, extra = {}) {
  const wrap = document.createElement("div");
  wrap.className = `message ${role}`;

  const avatar = createAvatar(role);
  wrap.appendChild(avatar);

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  if (extra.error) bubble.classList.add("error");

  if (extra.intent) {
    const tag = document.createElement("div");
    tag.className = "intent-tag";
    tag.textContent = INTENT_LABELS[extra.intent] || extra.intent;
    bubble.appendChild(tag);
  }

  if (extra.loading) {
    const typing = document.createElement("div");
    typing.className = "typing-indicator";
    typing.innerHTML = "<span></span><span></span><span></span>";
    bubble.appendChild(typing);
  } else if (extra.error || role === "user") {
    const body = document.createElement("p");
    body.textContent = text;
    bubble.appendChild(body);
  } else {
    const body = document.createElement("div");
    body.innerHTML = `<p>${formatText(text)}</p>`;
    bubble.appendChild(body);
  }

  wrap.appendChild(bubble);
  chat.appendChild(wrap);
  chat.scrollTop = chat.scrollHeight;
  return wrap;
}

function autoResizeTextarea() {
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 140) + "px";
}

async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/api/health`);
    const data = await res.json();
    if (data.status === "ok") {
      if (statDocs) statDocs.textContent = `${data.knowledge_docs} docs`;
      if (statModel) statModel.textContent = data.llm_provider;
      statusEl.textContent = data.api_key_configured ? "Connected" : "API key missing";
      if (data.password_required) {
        passwordInput.classList.remove("hidden");
        form.classList.add("has-password");
        passwordInput.placeholder = "Demo password (required)";
        passwordInput.required = true;
      }
    }
  } catch {
    statusEl.textContent = "Offline";
  }
}

async function sendMessage(message) {
  addMessage(message, "user");
  const loadingWrap = addMessage("", "bot", { loading: true });

  sendBtn.disabled = true;
  sendLabel.textContent = "...";

  try {
    const headers = { "Content-Type": "application/json" };
    const password = passwordInput.value.trim();
    const payload = { message };
    if (password) {
      headers.Authorization = `Bearer ${password}`;
      payload.password = password;
    }

    const res = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers,
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    loadingWrap.remove();

    if (!res.ok) {
      if (res.status === 401) {
        passwordInput.classList.remove("hidden");
        form.classList.add("has-password");
        passwordInput.required = true;
        addMessage(
          (data.error || "Password required") + " — enter it below and try again.",
          "bot",
          { error: true }
        );
        return;
      }
      addMessage(data.error || "Something went wrong.", "bot", { error: true });
      return;
    }

    addMessage(data.reply, "bot", { intent: data.intent });
  } catch (err) {
    loadingWrap.remove();
    addMessage(`Network error: ${err.message}`, "bot", { error: true });
  } finally {
    sendBtn.disabled = false;
    sendLabel.textContent = "Send";
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  input.value = "";
  input.style.height = "auto";
  sendMessage(message);
});

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    const prompt = chip.dataset.prompt;
    chip.style.transform = "scale(0.96)";
    setTimeout(() => { chip.style.transform = ""; }, 150);
    sendMessage(prompt);
  });
});

input.addEventListener("input", autoResizeTextarea);

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    form.requestSubmit();
  }
});

checkHealth();
