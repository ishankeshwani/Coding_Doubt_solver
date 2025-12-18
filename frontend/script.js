async function askAI() {
  const question = document.getElementById("question").value;
  const code = document.getElementById("code").value;
  const output = document.getElementById("output");

  output.innerText = "Thinking...";

  try {
    const response = await fetch(
      "https://coding-doubt-solver.onrender.com/api/ask",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question, code })
      }
    );

    const data = await response.json();
    console.log("Backend response:", data);

    if (data.answer) {
      output.innerText = data.answer;
    } else if (data.error) {
      output.innerText = "Backend error:\n" + data.error;
    } else {
      output.innerText = "Unexpected response from server.";
    }

  } catch (err) {
    console.error(err);
    output.innerText = "Could not reach AI server.";
  }
}