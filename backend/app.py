# backend/app.py
import os
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import json

# Load environment variables from .env
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Create FastAPI app and allow CORS for local dev
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # DEV: allow everything. In production, limit to your domain.
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to import and configure the official Gemini SDK; if not available, we'll use REST fallback
use_sdk = False
try:
    import google.generativeai as genai
    # configure SDK with the key from .env
    if GEMINI_KEY:
        genai.configure(api_key=GEMINI_KEY)
    else:
        print("Warning: GEMINI_API_KEY not found in .env; SDK may fail if used.")
    # Try model names available to your account
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
    except Exception:
        try:
            model = genai.GenerativeModel("models/gemini-2.5-pro")
        except Exception:
            model = None
    if model is not None:
        use_sdk = True
    else:
        print("Gemini SDK imported but could not create model handle; will use REST fallback.")
except Exception as e:
    print("Gemini SDK not available or failed to import:", repr(e))
    use_sdk = False

def call_gemini_rest(prompt: str) -> str:
    """REST fallback to call Gemini / Generative Language API.
    This uses the newer Generative Language endpoint pattern. If your Google project requires a different
    endpoint name or model id, change `model_name` accordingly.
    """
    if not GEMINI_KEY:
        return "Error: GEMINI_API_KEY not configured."

    # Choose model name you have access to. Common names: 'gemini-pro', 'gemini-1.5' etc.
    model_name = "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1/models/{model_name}:generateContent?key={GEMINI_KEY}"

    headers = {
        "Authorization": f"Bearer {GEMINI_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "prompt": {"text": prompt},
        "temperature": 0.0,
        "maxOutputTokens": 800
    }

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=30)
    except Exception as e:
        print("HTTP request to Gemini REST failed:", repr(e))
        raise

    if resp.status_code != 200:
        print("Gemini REST returned non-200:", resp.status_code, resp.text[:1000])
        return f"Gemini REST error {resp.status_code}: {resp.text}"

    jr = {}
    try:
        jr = resp.json()
    except Exception:
        # If response is not JSON (rare), return raw text
        return resp.text

    # Try known response shapes in order of likelihood
    # 1) modern Generative Language API: jr.get('candidates') or jr.get('output')
    if isinstance(jr, dict):
        # Try 'candidates' -> first candidate -> 'content' -> 'text'
        try:
            return jr.get('candidates', [{}])[0].get('content', {}).get('text', '') or str(jr)
        except Exception:
            pass
        # Try 'output' -> 'contents' or 'text'
        try:
            # variations: jr['output']['text'], jr['output']['contents'] etc.
            out = jr.get('output')
            if isinstance(out, dict):
                # try nested forms
                if 'text' in out:
                    return out['text']
                if 'contents' in out and isinstance(out['contents'], list) and len(out['contents'])>0:
                    # join text parts
                    pieces = []
                    for item in out['contents']:
                        if isinstance(item, dict) and 'text' in item:
                            pieces.append(item['text'])
                    if pieces:
                        return "\n".join(pieces)
        except Exception:
            pass

    # Fallback: return the whole JSON as string so caller can inspect
    return json.dumps(jr)

def call_gemini_sdk(prompt: str) -> str:
    """Call Gemini via the SDK. SDK methods change between versions; adapt if needed."""
    resp = model.generate_content(prompt)
    # SDK return shape may vary; try common attributes
    return getattr(resp, "text", "") or getattr(resp, "candidates", [{}])[0].get("content", {}).get("text", "")

def build_prompt(question: str, code: str) -> str:
    """Create a clear, few-shot prompt that asks the model to explain and patch code."""
    few_shot = (
        "Example:\n"
        "Q: TypeError: 'int' object is not iterable\n"
        "Code:\n"
        "x = 5\n"
        "for i in x:\n"
        "    print(i)\n"
        "A:\n"
        "1) Explanation: x is an int, not iterable.\n"
        "2) Suggested patch:\n"
        "```python\n"
        "x = [1,2,3]\n"
        "for i in x:\n"
        "    print(i)\n"
        "```\n\n"
    )
    prompt = (
        "You are a helpful coding assistant. For the user's question and code, return a structured answer:\n"
        "1) Explanation:\n2) Suggested patch (include only a python code block):\n3) Tests to run:\n4) Short notes/sources.\n\n"
        f"{few_shot}"
        f"User question:\n{question}\n\nCode:\n{code}\n\nAnswer:\n"
    )
    return prompt

@app.post("/api/ask")
async def ask(request: Request):
    """Main endpoint: expects JSON with keys 'question' and 'code'."""
    print("=== /api/ask called ===")
    try:
        body = await request.json()
    except Exception as e:
        print("ERROR reading json:", e)
        return JSONResponse({"error": "invalid json"}, status_code=400)

    print("BODY RECEIVED:", body)
    question = body.get("question", "")
    code = body.get("code", "")

    prompt = build_prompt(question, code)
    print("Built prompt (first 200 chars):", prompt[:200].replace("\n", "\\n"))

    # Call Gemini: prefer SDK if available, otherwise use REST fallback
    answer = ""
    if use_sdk:
        try:
            answer = call_gemini_sdk(prompt)
        except Exception as e:
            print("SDK call failed:", repr(e))
            # fallback to REST
            try:
                answer = call_gemini_rest(prompt)
            except Exception as e2:
                print("REST fallback failed:", repr(e2))
                return JSONResponse({"error": "LLM call failed"}, status_code=500)
    else:
        try:
            answer = call_gemini_rest(prompt)
        except Exception as e:
            print("REST call failed:", repr(e))
            return JSONResponse({"error": "LLM call failed"}, status_code=500)

    # Ensure we return a JSON object with a string answer
    if answer is None:
        answer = ""
    print("Gemini answer (first 400 chars):", str(answer)[:400].replace("\n", "\\n"))
    return JSONResponse({"answer": str(answer)})