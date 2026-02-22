import os
import io
import uuid
import numpy as np
import soundfile as sf
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from kokoro_onnx import Kokoro

import builtins
import numpy as np

# Fix for Kokoro-ONNX on Windows: Force UTF-8 for text files
_original_open = builtins.open
def _patched_open(*args, **kwargs):
    if len(args) > 1 and 'b' in args[1]:
        return _original_open(*args, **kwargs)
    if 'mode' in kwargs and 'b' in kwargs['mode']:
        return _original_open(*args, **kwargs)
    if 'encoding' not in kwargs:
        kwargs['encoding'] = 'utf-8'
    return _original_open(*args, **kwargs)
builtins.open = _patched_open

# Fix for Kokoro-ONNX: Allow pickle for voices.bin
_original_load = np.load
def _patched_load(*args, **kwargs):
    if 'allow_pickle' not in kwargs:
        kwargs['allow_pickle'] = True
    return _original_load(*args, **kwargs)
np.load = _patched_load

app = FastAPI()

# Configuration
MODEL_PATH = "kokoro-v0_19.onnx"
VOICES_PATH = "voices.bin"

# Initialize Kokoro
# Note: We'll initialize lazily to avoid error if files are still downloading
kokoro_engine = None

def get_engine():
    global kokoro_engine
    if kokoro_engine is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(VOICES_PATH):
            raise RuntimeError("Model or Voices file missing. Please ensure download is complete.")
        kokoro_engine = Kokoro(MODEL_PATH, VOICES_PATH)
    return kokoro_engine

class TTSRequest(BaseModel):
    text: str
    voice: str = "bm_george" # UK Male voice

@app.post("/generate")
async def generate_tts(request: TTSRequest):
    try:
        engine = get_engine()
        samples, sample_rate = engine.create(
            request.text, voice=request.voice, speed=1.0, lang="en-gb"
        )
        
        # Save to memory instead of disk
        buffer = io.BytesIO()
        sf.write(buffer, samples, sample_rate, format='mp3')
        buffer.seek(0)
        
        return StreamingResponse(buffer, media_type="audio/mpeg")
        
    except Exception as e:
        print(f"TTS Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    try:
        get_engine()
        return {"status": "ok", "service": "kokoro-onnx-local"}
    except Exception as e:
        return {"status": "initializing", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8880)
