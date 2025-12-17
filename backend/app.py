import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()

# ✅ CORS (ALLOW EVERYTHING – SAFE FOR COLLEGE PROJECT)
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

# ✅ Explicit OPTIONS handler (THIS FIXES PREFLIGHT FAILURES)
@app.options("/api/ask")
def options_ask():
    return {}

@app.get("/")
def root():
    return {"status": "Backend is running"}

@app.post("/api/ask")
def ask_ai(data: AskRequest):
    try:
        prompt = f"""
You are a helpful coding assistant.

Question:
{data.question}

Code:
{data.code}

Explain clearly and suggest a fix.
"""

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        return {"answer": completion.choices[0].message.content}

    except Exception as e:
        # IMPORTANT: return error instead of crashing
        return {"error": str(e)}