const BACKEND_URL = "https://coding-doubt-solver.onrender.com/api/ask";

async function askAI() {
  const question = document.getElementById("question").value;
  const code = document.getElementById("code").value;
  const output = document.getElementById("output");

  output.innerText = "Thinking...";

  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question: question,
        code: code
      })
    });

    if (!response.ok) {
      throw new Error("Server error");
    }

    const data = await response.json();   // 🔥 THIS WAS MISSING

    output.innerText = data.answer;        // 🔥 NOW IT WORKS
  }
  catch (err) {
    output.innerText = "❌ Could not reach AI server.";
    console.error(err);
  }
}

async function runCode() {
  const code = document.getElementById("code").value;
  const output = document.getElementById("output");

  try {
    if (!window.pyodide) {
      window.pyodide = await loadPyodide();
    }

    let result = await pyodide.runPythonAsync(code);
    output.innerText = result ?? "Code executed.";
  }
  catch (err) {
    output.innerText = err.toString();
  }
}