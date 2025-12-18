import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.post("/api/ask")
def ask_ai(data: dict):
    language = data.get("language", "Python")
    line = "Explain line by line." if data.get("lineByLine") else "Explain simply."

    prompt = f"""
You are an expert {language} programming tutor.

{line}

Question:
{data.get("question")}

Code:
{data.get("code")}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return {"answer": response.choices[0].message.content}