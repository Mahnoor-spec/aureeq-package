import httpx
import asyncio

async def verify_hallucinations_and_scope():
    async with httpx.AsyncClient(timeout=120.0) as client:
        test_cases = [
            ("where are you located?", "plain_address"),
            ("what is the weather outside?", "scope_refusal"),
            ("suggest me something to eat", "variety_mains"),
            ("i want a chicken platter", "out_of_menu")
        ]
        
        for q, label in test_cases:
            print(f"\n--- Testing Query ({label}): '{q}' ---")
            try:
                res = await client.post("http://127.0.0.1:8001/chat", json={"message": q, "user_id": "test_final_verify"})
                full_text = ""
                async for chunk in res.aiter_text():
                    full_text += chunk
                
                print(f"Response: {full_text}")
                
                # Checks
                if label == "plain_address":
                    if "http" in full_text.split("located at")[1]:
                        print(">>> FAILURE: Address still contains a link.")
                    else:
                        print(">>> SUCCESS: Address is plain text.")
                
                if label == "scope_refusal":
                    if "weather" in full_text.lower() and ("sunny" in full_text.lower() or "lovely" in full_text.lower() or "bright" in full_text.lower()):
                         print(">>> FAILURE: AI is still talking about the weather.")
                    else:
                         print(">>> SUCCESS: AI refused or successfully pivoted out of scope.")
                         
                if label == "variety_mains":
                    # Check if at least one Main category dish is suggested (e.g., Lamb, Chicken, Seafood)
                    # This is indicative
                    lower_text = full_text.lower()
                    if "lamb kebab barg" in lower_text or "ranjha gosht" in lower_text or "sea bass" in lower_text:
                         print(">>> SUCCESS: Diverse suggestions including mains found!")
                    else:
                         print(">>> WARNING: Might still be stuck in Mezze or restricted context.")
                
                if "pomegranate juice" in full_text.lower() or "chicken platter" in full_text.lower():
                     print(">>> FAILURE: Hallucination detected!")

            except Exception as e:
                print(f">>> ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(verify_hallucinations_and_scope())
