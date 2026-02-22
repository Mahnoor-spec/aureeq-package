import httpx
import asyncio

async def test_user_queries():
    async with httpx.AsyncClient(timeout=30.0) as client:
        queries = [
            "chicken items from starters",
            "show m ethe chicken options from starter",
            "i want to make a reservaton",
            "give me anything from bbq",
            "what do you have in dessert?"
        ]
        
        for q in queries:
            print(f"\n--- Testing Query: '{q}' ---")
            try:
                res = await client.post("http://127.0.0.1:8001/chat", json={"message": q, "user_id": "test_user"})
                full_text = ""
                async for chunk in res.aiter_text():
                    full_text += chunk
                
                print(f"Response: {full_text[:200]}...") # Print first 200 chars
                
                if "error" in full_text.lower() or "connection issue" in full_text.lower():
                    print(f">>> FAILURE: Error detected in response for '{q}'")
                elif not full_text:
                    print(f">>> FAILURE: Empty response for '{q}'")
                else:
                    print(f">>> SUCCESS: Received valid response for '{q}'")
            except Exception as e:
                print(f">>> ERROR: Request failed for '{q}': {e}")

if __name__ == "__main__":
    asyncio.run(test_user_queries())
