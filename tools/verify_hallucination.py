import httpx
import asyncio
import sys

# Ensure stdout uses UTF-8 to handle any special characters
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

async def verify_hallucination():
    user_id = f"test_user_hallucination_{asyncio.get_event_loop().time()}"
    base_url = "http://127.0.0.1:8002"

    print("\n--- ROBUST VERIFICATION: ANTI-HALLUCINATION ---\n")

    query = "we have a budget of 30 for the whole group not per head"
    print(f"Query: {query}")

    async with httpx.AsyncClient(timeout=300.0) as client:
        # Step 1: Initialize welcome
        await client.get(f"{base_url}/welcome?name=Mahnoor&user_id={user_id}")
        
        # Step 2: Streaming Chat
        async with client.stream("POST", f"{base_url}/chat", json={
            "user_id": user_id,
            "message": query,
            "was_voice": False
        }) as resp:
            full_response = ""
            async for chunk in resp.aiter_text():
                if chunk:
                    full_response += chunk
                    # Print immediately to show progress
                    sys.stdout.write(chunk)
                    sys.stdout.flush()

        print(f"\n\n--- ANALYSIS ---\n")

        # CHECK 1: Presence of "Grilled Meat Platter" (Hallucination)
        if "Grilled Meat Platter" in full_response:
            print("FAILURE: Hallucination detected ('Grilled Meat Platter' found)!")
        else:
            print("SUCCESS: No 'Grilled Meat Platter' hallucinated.")

        # CHECK 2: Grounding
        # Bannu Pulao is 15.99, Lamb Chops 25.99, etc.
        if "Bannu Pulao" in full_response and "15.99" in full_response:
            print("SUCCESS: Correctly grounded Bannu Pulao with price.")
        
        if "£" in full_response:
            print("SUCCESS: Prices present.")
        else:
            print("FAILURE: Prices missing.")

if __name__ == "__main__":
    asyncio.run(verify_hallucination())
