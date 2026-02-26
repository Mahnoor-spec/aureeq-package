import os
import json
import asyncio
import traceback
import uuid
import base64
from typing import Optional, List, Dict
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Modular components
import order_db
from rag_engine import RAGEngine
from phi_handler import PhiHandler
from llama_handler import LlamaHandler
from memory_manager import MemoryManager
from streaming_engine import StreamingEngine
import hardcode_rules as rules

# --- CONFIGURATION ---
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8001")
OLLAMA_HOST_URL = os.getenv("AUREEQ_OLLAMA_URL") or os.getenv("OLLAMA_HOST") or "http://127.0.0.1:11434"
TTS_HOST_URL = os.getenv("AUREEQ_TTS_URL") or os.getenv("TTS_HOST") or "http://127.0.0.1:8880"
SYNC_INTERVAL = int(os.getenv("SYNC_INTERVAL_HOURS", "24"))

# Normalize URLs
if "0.0.0.0" in OLLAMA_HOST_URL: 
    OLLAMA_HOST_URL = OLLAMA_HOST_URL.replace("0.0.0.0", "127.0.0.1")
if "0.0.0.0" in TTS_HOST_URL: 
    TTS_HOST_URL = TTS_HOST_URL.replace("0.0.0.0", "127.0.0.1")

if not OLLAMA_HOST_URL.startswith("http"): 
    OLLAMA_HOST_URL = f"http://{OLLAMA_HOST_URL}"
if not TTS_HOST_URL.startswith("http"): 
    TTS_HOST_URL = f"http://{TTS_HOST_URL}"

MODEL_EMBED = os.getenv("MODEL_EMBED", "nomic-embed-text")
MODEL_PHI = os.getenv("MODEL_PHI", "phi3:mini")
MODEL_LLAMA = os.getenv("MODEL_LLAMA", "llama3.3:latest")

print(f"DEBUG: Using Model {MODEL_LLAMA} at {OLLAMA_HOST_URL}", flush=True)

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
MENU_JSON_PATH = os.path.join(DATA_DIR, "menu.json")
EXAMPLES_TXT_PATH = os.path.join(DATA_DIR, "sales_examples_new.txt")

async def background_menu_sync():
    """Background task to sync menu from WordPress every 24 hours."""
    from sync_wp_menu import sync_menu
    while True:
        try:
            print(f"Starting scheduled menu sync (Interval: {SYNC_INTERVAL}h)...", flush=True)
            success = await sync_menu()
            if success and ENGINE:
                await ENGINE.refresh_data()
                print("Menu synced and RAG refreshed in background.", flush=True)
        except Exception as e:
            print(f"Background Sync Error: {e}", flush=True)
        
        await asyncio.sleep(SYNC_INTERVAL * 3600)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global ENGINE, HTTP_CLIENT
    print("Initializing Aureeq Backend Inference System...", flush=True)
    
    # Init HTTP Client
    HTTP_CLIENT = httpx.AsyncClient(timeout=30.0, trust_env=False)
    
    # Warm up TTS
    try:
        print(f"Warming up TTS engine at {TTS_HOST_URL}...", flush=True)
        # Use health check or just a small generate call
        resp = await HTTP_CLIENT.get(f"{TTS_HOST_URL}/health")
        if resp.status_code == 200:
            print(f"TTS Health: {resp.json()}", flush=True)
    except:
        print("TTS Engine not found or warming failed.", flush=True)

    # Init Sub-engines
    rag = RAGEngine(MENU_JSON_PATH, EXAMPLES_TXT_PATH, OLLAMA_HOST_URL, MODEL_EMBED)
    
    # Load Initial Data
    await rag.init_menu() # Re-embeds Everything
    
    phi = PhiHandler(OLLAMA_HOST_URL, MODEL_PHI, rag.menu_data)
    llama = LlamaHandler(OLLAMA_HOST_URL, MODEL_LLAMA, rag.menu_data)
    memory = MemoryManager()
    
    ENGINE = StreamingEngine(rag, memory, phi, llama)
    
    # Start Background Sync
    asyncio.create_task(background_menu_sync())
    
    yield
    # Shutdown
    await HTTP_CLIENT.aclose()
    print("Shutting down...", flush=True)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
ENGINE: Optional[StreamingEngine] = None
HTTP_CLIENT: Optional[httpx.AsyncClient] = None

class ChatRequest(BaseModel):
    message: str
    user_id: str
    was_voice: bool = False
    language: str = "en"

class TTSRequest(BaseModel):
    text: str
    language: str = "en-us"

# Health Check
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/api/welcome")
@app.get("/welcome")
async def welcome_endpoint(name: str, user_id: str = "guest", language: str = "en"):
    """Generate welcome message and audio"""
    if language == 'ar':
        # exact syntax requested by user for display
        response_text = f"مرحباً {name}، أنا AUREEQ مساعدك الشخصي. كيف يمكنني مساعدتك اليوم؟"
        # Spoken text uses Arabic for brand name to ensure proper TTS pronunciation
        spoken_text = f"مرحباً {name}، أنا أورِيق مساعدك الشخصي. كيف يمكنني مساعدتك اليوم؟"
    else:
        response_text = f"Hello {name}, I am AUREEQ your personal assistant. How may I help you today?"
        spoken_text = response_text
        
    print(f"DEBUG: Generating welcome text [{language}]", flush=True)
    
    # Save to memory to ensure history_len > 0 for Turn 1
    if ENGINE:
        ENGINE.save_to_memory(user_id, "[Onboarding]", response_text)
    
    audio_b64 = None
    if HTTP_CLIENT:
        try:
            remote_url = f"{TTS_HOST_URL}/generate"
            payload = {
                "text": spoken_text,
                "voice": "am_adam" if language == 'ar' else "af_sky",
                "lang_code": "ar" if language == 'ar' else "en-us"
            }
            resp = await HTTP_CLIENT.post(remote_url, json=payload, timeout=15)
            if resp.status_code == 200:
                b64 = base64.b64encode(resp.content).decode('utf-8')
                audio_b64 = f"data:audio/wav;base64,{b64}"
            else:
                print(f"TTS Greeting Failed with status {resp.status_code}")
        except Exception as e:
            print(f"Welcome Audio Generation Failed: {e}")

    return JSONResponse({"response": response_text, "audio_url": audio_b64})

@app.post("/api/chat")
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not ENGINE:
        raise HTTPException(status_code=503, detail="Server initializing")
    
    # SELECTIVE AUDIO TRIGGER
    session = ENGINE.memory.get_session(request.user_id)
    history = session.get_history()
    # Turn tracking: If history exists from welcome, history_len will be >= 2.
    # We only play audio if history is empty (impossible if welcome ran) or if it's voice.
    # Note: history_len counts messages, 2 messages per turn.
    should_audio = (len(history) == 0) or request.was_voice
    
    print(f"DEBUG: Chat request: {request.message}. HistoryLen: {len(history)}, WasVoice: {request.was_voice}, ShouldAudio: {should_audio}", flush=True)

    async def generate_and_stream():
        full_response = ""
        token_count = 0
        try:
            async for chunk in ENGINE.generate_response(request.user_id, request.message, request.language):
                if chunk:
                    # STRICT RULE: No symbols in responses
                    cleaned_chunk = chunk.replace("*", "").replace("#", "")
                    token_count += 1
                    full_response += cleaned_chunk
                    yield cleaned_chunk

            # If no tokens were generated, provide a friendly fallback
            if token_count == 0:
                fallback_resp = rules.RESP_FALLBACK_RECOMMENDATION
                full_response = fallback_resp
                yield fallback_resp
            
            # Save to memory AFTER streaming (Handled here now)
            ENGINE.save_to_memory(request.user_id, request.message, full_response.strip())

            # Selective TTS logic:
            if full_response.strip() and should_audio:
                print(f"DEBUG: Selective TTS Triggered.")
                audio_url = "/tts" 
                yield f"|AUDIO_URL|{audio_url}|TEXT|{full_response.strip()}"

        except Exception as e:
            print(f"Chat error: {e}")
            traceback.print_exc()
            yield "I encountered a slight technical hitch. How else can I help you?"

    return StreamingResponse(generate_and_stream(), media_type="text/event-stream")

@app.post("/api/tts")
@app.post("/tts")
async def tts_endpoint(request: TTSRequest):
    """Proxy to the actual TTS engine"""
    if not HTTP_CLIENT:
        raise HTTPException(status_code=503, detail="HTTP Client not ready")
        
    try:
        remote_url = f"{TTS_HOST_URL}/generate"
        if request.language == 'ar':
            voice = "am_adam"
            lang_code = "ar"
        else:
            voice = os.getenv("TTS_VOICE", "bm_george")
            lang_code = "en-gb"
            
        payload = {"text": request.text, "voice": voice, "lang": lang_code}
        
        resp = await HTTP_CLIENT.post(remote_url, json=payload, timeout=15)
        if resp.status_code == 200:
            return StreamingResponse(resp.iter_bytes(), media_type="audio/wav")
        else:
            raise HTTPException(status_code=resp.status_code, detail="TTS Generation Failed")
    except Exception as e:
        print(f"TTS Proxy Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Use port from env if available
    port = int(os.getenv("BACKEND_PORT", "8002"))
    uvicorn.run(app, host="0.0.0.0", port=port)
