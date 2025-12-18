async function askAI() {
  const output = document.getElementById("output");
  const loader = document.getElementById("loader");

  const question = document.getElementById("question").value;
  const code = document.getElementById("code").value;
  const language = document.getElementById("language").value;
  const lineByLine = document.getElementById("lineByLine").checked;

  output.innerText = "";
  loader.style.display = "block";

  try {
    const response = await fetch(
      "https://coding-doubt-solver.onrender.com/api/ask",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, code, language, lineByLine })
      }
    );

    const data = await response.json();
    output.innerText = data.answer || data.error;

  } catch {
    output.innerText = "Could not reach AI server.";
  }

  loader.style.display = "none";
}

function clearAll() {
  document.getElementById("question").value = "";
  document.getElementById("code").value = "";
  document.getElementById("output").innerText = "";
}

function copyOutput() {
  const text = document.getElementById("output").innerText;
  navigator.clipboard.writeText(text);
  alert("Output copied!");
}