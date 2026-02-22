from kokoro_onnx import Kokoro
import os

models = ["kokoro_v019.onnx", "kokoro-v0_19.onnx"]
voices = ["voices_v1.bin", "voices.bin"]

for m in models:
    for v in voices:
        print(f"\n--- Testing Model: {m}, Voices: {v} ---")
        if not os.path.exists(m) or not os.path.exists(v):
            print("Skip: File missing")
            continue
        try:
            engine = Kokoro(m, v)
            print("SUCCESS!")
        except Exception as e:
            print(f"FAILED: {e}")
