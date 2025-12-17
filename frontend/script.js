const askBtn = document.getElementById("askBtn");
const output = document.getElementById("output");

askBtn.addEventListener("click", async () => {
  const question = document.getElementById("question").value;
  const code = document.getElementById("code").value;

  output.innerText = "⏳ Thinking...";

  try {
    const response = await fetch(
      "https://coding-doubt-solver.onrender.com/api/ask",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
          code: code,
        }),
      }
    );

    const data = await response.json();

    // ✅ THIS IS THE KEY FIX
    output.innerText = data.answer || "No response from AI";

  } catch (error) {
    console.error(error);
    output.innerText = "❌ Could not reach AI server.";
  }
});