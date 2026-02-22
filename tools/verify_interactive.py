import httpx
import asyncio

async def verify_interactivity():
    async with httpx.AsyncClient(timeout=60.0) as client:
        test_cases = [
            ("i want to buy iphone", "gadget"),
            ("i am hungry", "persuasive"),
            ("we are a group of 5 and have a budget of 30", "budget plan"),
            ("suggest me something to eat", "recommendation")
        ]
        
        for q, expected in test_cases:
            print(f"\n--- Testing Query: '{q}' ---")
            try:
                res = await client.post("http://127.0.0.1:8001/chat", json={"message": q, "user_id": "test_user_new"})
                full_text = ""
                async for chunk in res.aiter_text():
                    full_text += chunk
                
                print(f"Response: {full_text}")
                
                if "connection issue" in full_text.lower():
                    print(">>> FAILURE: Connection issue fallback triggered.")
                elif "full menu" in full_text.lower() and q == "i am hungry":
                     print(">>> WARNING: Still returning full menu for 'hungry' - check router.")
                else:
                    print(f">>> SUCCESS: Received response for '{q}'")
            except Exception as e:
                print(f">>> ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(verify_interactivity())
