const askBtn = document.getElementById("askBtn");
const output = document.getElementById("output");

askBtn.addEventListener("click", async () => {
  const question = document.getElementById("question").value;
  const code = document.getElementById("code").value;

  output.innerText = "Thinking...";

  try {
    const res = await fetch("https://coding-doubt-solver.onrender.com/api/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question: question,
        code: code
      })
    });

    const data = await res.json();
    output.innerText = data.answer;

  } catch (err) {
    output.innerText = "Error connecting to AI server";
  }
});