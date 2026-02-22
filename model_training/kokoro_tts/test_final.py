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

model = "kokoro-v0_19.onnx"
voices = "voices.json"

print(f"Testing Model: {model}, Voices: {voices}")
try:
    engine = Kokoro(model, voices)
    print("SUCCESS! Engine ready.")
except Exception as e:
    import traceback
    print(f"FAILED: {e}")
    traceback.print_exc()
