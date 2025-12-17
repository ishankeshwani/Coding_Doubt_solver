import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()

# ✅ CORS — allow all during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return {"status": "Backend is running 🚀"}

@app.post("/api/ask")
def ask_ai(data: AskRequest):
    prompt = f"""
You are a helpful coding tutor.

Question:
{data.question}

Code:
{data.code}

Explain clearly and simply.
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return {
        "answer": response.choices[0].message.content
    }