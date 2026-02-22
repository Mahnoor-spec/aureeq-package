import builtins
# Monkeypatch
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
