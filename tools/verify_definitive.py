import httpx
import asyncio
import json

async def verify_final():
    user_id = f"test_user_{asyncio.get_event_loop().time()}"
    base_url = "http://127.0.0.1:8002"

    print("\n--- NEW DEFINITIVE VERIFICATION: AUDIO & CART IDs ---\n")

    # 1. SITE LOAD: Welcome Greeting (Turn 0)
    # Expected: AUDIBLE URL returned
    print("TURN 0: Welcome Greeting")
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(f"{base_url}/welcome?name=Mahnoor&user_id={user_id}")
        data = resp.json()
        if data.get("audio_url"):
            print("  Result: AUDIBLE (Matched)")
        else:
            print("  Result: SILENT (Mismatch!)")

    # 2. TURN 1: Typed Chat (Expected: Silent)
    # Since Welcome was Turn 0 and saved to memory, Turn 1 should be silent.
    print("\nTURN 1: First Typed Chat (Expected: Silent)")
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(f"{base_url}/chat", json={
            "user_id": user_id,
            "message": "tell me about lamb chops",
            "was_voice": False
        })
        text = resp.text
        if "|AUDIO_URL|" in text:
            print(f"  Result: AUDIBLE (Mismatch!) -> {text}")
        else:
            print("  Result: SILENT (Matched)")

    # 3. TURN 2: Voice Chat (Expected: Audible)
    print("\nTURN 2: Voice Chat (Expected: Audible)")
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(f"{base_url}/chat", json={
            "user_id": user_id,
            "message": "add lamb chops",
            "was_voice": True
        })
        text = resp.text
        if "|AUDIO_URL|" in text:
            print("  Result: AUDIBLE (Matched)")
        else:
            print("  Result: SILENT (Mismatch!)")

    # 4. TURN 3: Cart ID Priority Check
    # "add baklava" - BAKLAVA is a dessert keyword, but ADD is a cart keyword.
    # Expected: [ORDER] tag returned.
    print("\nTURN 3: Cart Priority Check (Add Baklava)")
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(f"{base_url}/chat", json={
            "user_id": user_id,
            "message": "add to cart baklava",
            "was_voice": False
        })
        text = resp.text
        if "[ORDER: Baklava |" in text:
            print(f"  Result: Cart Tag Found! (Matched) -> {text}")
        else:
            print(f"  Result: Cart Tag MISSING! (Mismatch!) -> {text}")

if __name__ == "__main__":
    asyncio.run(verify_final())
