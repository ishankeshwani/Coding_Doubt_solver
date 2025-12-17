let pyodide = null;

// Load Pyodide silently
async function initPyodide() {
  pyodide = await loadPyodide();
}
initPyodide();

function showOutput(text) {
  document.getElementById("output").innerText = text;
}

// Run Python code
async function runCode() {
  const code = document.getElementById("code").value;
  if (!code.trim()) {
    showOutput("⚠️ Please enter some Python code.");
    return;
  }

  try {
    const result = await pyodide.runPythonAsync(code);
    showOutput(result !== undefined ? result : "✅ Code executed successfully.");
  } catch (err) {
    showOutput("❌ Error:\n" + err);
  }
}

// Ask AI (clean UI)
async function askAI() {
  const question = document.getElementById("question").value;
  const code = document.getElementById("code").value;

  if (!question.trim()) {
    showOutput("⚠️ Please enter a question.");
    return;
  }

  showOutput("🤖 Thinking...");

  try {
    const res = await fetch("http://coding-doubt-solver.onrender.com/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, code })
    });

    const data = await res.json();
    showOutput(data.answer);

  } catch (err) {
    showOutput("❌ Could not reach AI server.");
  }
}