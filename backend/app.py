import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()

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
    return {"status": "Backend running"}

@app.post("/api/ask")
def ask_ai(data: AskRequest):
    try:
        prompt = f"""
You are a helpful coding assistant.

Question:
{data.question}

Code:
{data.code}

Explain the issue clearly and suggest a fix.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )

        return {"answer": response.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}