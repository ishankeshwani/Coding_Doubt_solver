import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read environment variables
PROVIDER = os.getenv("PROVIDER")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize FastAPI
app = FastAPI()

# ✅ CORS FIX (THIS SOLVES YOUR ISSUE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://codingdoubtsolver.netlify.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Request body model
class AskRequest(BaseModel):
    question: str
    code: str

# Health check (optional but useful)
@app.get("/")
def root():
    return {"status": "Backend is running 🚀"}

# Main AI endpoint
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
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return {
        "answer": response.choices[0].message.content
    }