import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# Load environment variables (works locally; ignored on Render)
load_dotenv()

# Read Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# ✅ CORS CONFIGURATION (THIS FIXES YOUR ERROR)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins (OK for college project)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Request body schema
class AskRequest(BaseModel):
    question: str
    code: str

# Root endpoint (health check)
@app.get("/")
def root():
    return {"status": "Backend is running"}

# Main AI endpoint
@app.post("/api/ask")
def ask_ai(data: AskRequest):
    prompt = f"""
You are a helpful coding assistant.

Question:
{data.question}

Code:
{data.code}

Explain the issue clearly and suggest a fix.
"""

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return {
        "answer": completion.choices[0].message.content
    }