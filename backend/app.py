from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

# Create FastAPI app
app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # OK for college project
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read Groq API key from environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Data format coming from frontend
class AskRequest(BaseModel):
    question: str
    code: str

@app.post("/api/ask")
async def ask_ai(data: AskRequest):
    prompt = f"""
You are a helpful coding assistant.

Question:
{data.question}

Code:
{data.code}

Explain the mistake clearly and provide corrected code.
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "answer": response.choices[0].message.content
    }