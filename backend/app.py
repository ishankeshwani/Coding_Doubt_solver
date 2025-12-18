import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# Load env variables
load_dotenv()

PROVIDER = os.getenv("PROVIDER")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()

# ✅ CORS (CORRECT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://codingdoubtsolver.netlify.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=GROQ_API_KEY)

class AskRequest(BaseModel):
    question: str
    code: str

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.post("/api/ask")
def ask_ai(data: AskRequest):
    if PROVIDER != "GROQ":
        return {"error": "Invalid provider"}

    prompt = f"""
You are a helpful coding tutor.

Question:
{data.question}

Code:
{data.code}

Explain clearly and simply.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ FIXED MODEL
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return {
        "answer": response.choices[0].message.content
    }