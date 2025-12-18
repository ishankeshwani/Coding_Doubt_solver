const output = document.getElementById("output");

async function askAI() {
  output.innerText = "Thinking... 🤔";

  const question = document.getElementById("question").value;
  const code = document.getElementById("code").value;

  try {
    const response = await fetch(
      "https://coding-doubt-solver.onrender.com/api/ask",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          question: question,
          code: code
        })
      }
    );

    const data = await response.json();

    // ✅ THIS IS THE KEY FIX
    output.innerText = data.answer || "No response from AI.";

  } catch (error) {
    output.innerText = "Could not reach AI server.";
    console.error(error);
  }
}