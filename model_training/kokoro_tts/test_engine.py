from kokoro_onnx import Kokoro
import os

MODEL_PATH = "kokoro_v019.onnx"
VOICES_PATH = "voices_v1.bin"

print(f"Testing Kokoro with {MODEL_PATH} and {VOICES_PATH}...")
print(f"Exists? Model: {os.path.exists(MODEL_PATH)}, Voices: {os.path.exists(VOICES_PATH)}")

try:
    engine = Kokoro(MODEL_PATH, VOICES_PATH)
    print("Engine initialized successfully!")
    
    print("Testing Arabic generation with am_adam...")
    samples, sample_rate = engine.create("مرحباً", voice="am_adam", speed=1.0, lang="ar")
    print(f"Success! Generated {len(samples)} samples at {sample_rate}Hz")
    
except Exception as e:
    import traceback
    print(f"Failed: {e}")
    traceback.print_exc()
