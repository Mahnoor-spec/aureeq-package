from kokoro_onnx import Kokoro
import os

MODEL_PATH = "kokoro_v019.onnx"
VOICES_PATH = "voices_v1.bin"

print(f"Testing Kokoro with {MODEL_PATH} and {VOICES_PATH}...")
print(f"Exists? Model: {os.path.exists(MODEL_PATH)}, Voices: {os.path.exists(VOICES_PATH)}")

try:
    engine = Kokoro(MODEL_PATH, VOICES_PATH)
    print("Engine initialized successfully!")
except Exception as e:
    import traceback
    print(f"Failed to initialize engine: {e}")
    traceback.print_exc()
