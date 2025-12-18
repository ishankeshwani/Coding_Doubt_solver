let pyodideReady = false;

async function initPyodide() {
  self.pyodide = await loadPyodide();
  pyodideReady = true;
}
initPyodide();

function showLoader(show) {
  document.getElementById("loader").classList.toggle("hidden", !show);
}

function runCode() {
  const code = document.getElementById("code").value;
  const output = document.getElementById("output");

  if (!pyodideReady) {
    output.textContent = "Loading Python...";
    return;
  }

  try {
    output.textContent = pyodide.runPython(code);
  } catch (err) {
    output.textContent = err;
  }
}

async function askAI() {
  const output = document.getElementById("output");
  showLoader(true);
  output.textContent = "";

  const res = await fetch("https://coding-doubt-solver.onrender.com/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question: document.getElementById("question").value,
      code: document.getElementById("code").value
    })
  });

  const data = await res.json();
  showLoader(false);

  output.textContent = data.answer || "No response";
  document.querySelector(".copy").classList.remove("hidden");
}

function clearAll() {
  document.getElementById("question").value = "";
  document.getElementById("code").value = "";
  document.getElementById("output").textContent = "";
  document.querySelector(".copy").classList.add("hidden");
}

function copyOutput() {
  navigator.clipboard.writeText(
    document.getElementById("output").textContent
  );
  alert("Copied to clipboard!");
}