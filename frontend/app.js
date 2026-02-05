const API = "http://127.0.0.1:8000";

const chatWindow = document.getElementById("chatWindow");
const input = document.getElementById("msgInput");
const fileInput = document.getElementById("fileInput");
const status = document.getElementById("uploadStatus");
const dropZone = document.getElementById("dropZone");

let chatMemory = JSON.parse(localStorage.getItem("chatMemory") || "[]");

/* ---------- RESTORE CHAT ON LOAD ---------- */

chatMemory.forEach(m => renderMsg(m.role, m.text));

function saveMemory() {
  localStorage.setItem("chatMemory", JSON.stringify(chatMemory));
}

/* ---------- MESSAGE UI ---------- */

function renderMsg(role, text) {
  const div = document.createElement("div");
  div.className = "msg " + role;
  div.innerText = text;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function addMsg(role, text) {
  chatMemory.push({ role, text });
  saveMemory();
  renderMsg(role, text);
}

function updateLastBot(text) {
  const bots = document.querySelectorAll(".msg.bot");
  bots[bots.length - 1].innerText = text;
  chatMemory[chatMemory.length - 1].text = text;
  saveMemory();
}

/* ---------- FILE PICK ---------- */

function pickFiles() {
  fileInput.click();
}

fileInput.addEventListener("change", uploadFiles);

/* ---------- DRAG DROP ---------- */

dropZone.addEventListener("dragover", e => {
  e.preventDefault();
  dropZone.classList.add("drag");
});

dropZone.addEventListener("drop", e => {
  e.preventDefault();
  uploadFiles({ target: { files: e.dataTransfer.files } });
});

/* ---------- UPLOAD ---------- */

async function uploadFiles(e) {
  const files = e.target.files;
  if (!files.length) return;

  status.innerText = "Indexing…";

  for (let f of files) {
    const fd = new FormData();
    fd.append("file", f);

    await fetch(API + "/upload", {
      method: "POST",
      body: fd
    });
  }

  status.innerText = "✅ Indexed";
    refreshFiles();

}

/* ---------- CHAT ---------- */

async function send() {
  const text = input.value.trim();
  if (!text) return;

  addMsg("user", text);
  input.value = "";

  addMsg("bot", "Thinking…");

  try {

    const r = await fetch(API + "/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        message: text,
        memory: chatMemory
      })
    });

    if (!r.ok) {
      updateLastBot("❌ Server error");
      return;
    }

    const reader = r.body.getReader();
    const decoder = new TextDecoder();

    let out = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      out += decoder.decode(value);
      updateLastBot(out);
    }

  } catch (err) {
    updateLastBot("❌ Cannot reach backend");
  }
}

input.addEventListener("keydown", e => {
  if (e.key === "Enter") send();
});

async function refreshFiles(){
  const r = await fetch(API + "/files");
  const data = await r.json();

  const ul = document.getElementById("fileList");
  ul.innerHTML = "";

  data.files.forEach(f=>{
    const li = document.createElement("li");
    li.innerText = f;
    ul.appendChild(li);
  });
}

refreshFiles();
