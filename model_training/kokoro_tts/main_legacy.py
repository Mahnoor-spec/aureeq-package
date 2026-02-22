import os
import io
import uuid
import soundfile as sf
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from kokoro import KPipeline
import torch

app = FastAPI()

# Initialize Pipeline
# 'a' for American English
pipeline = KPipeline(lang_code='a')

class TTSRequest(BaseModel):
    text: str
    voice: str = "am_michael" # Smooth US Male voice

@app.post("/generate")
async def generate_tts(request: TTSRequest):
    try:
        # Generate audio
        # Kokoro returns a generator of (graphemes, phonemes, audio)
        generator = pipeline(
            request.text, voice=request.voice, 
            speed=1, split_pattern=r'\n+'
        )
        
        # Combine all audio chunks
        import numpy as np
        all_audio = []
        for gs, ps, audio in generator:
            all_audio.append(audio)
        
        if not all_audio:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
            
        combined_audio = np.concatenate(all_audio)
        
        # Save to memory instead of disk for speed
        buffer = io.BytesIO()
        sf.write(buffer, combined_audio, 24000, format='mp3')
        buffer.seek(0)
        
        return StreamingResponse(buffer, media_type="audio/mpeg")
        
    except Exception as e:
        print(f"TTS Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "service": "kokoro-tts"}
