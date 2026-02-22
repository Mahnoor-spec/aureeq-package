import httpx
import asyncio
import json

PROMPTS = [
    # GREETINGS & IDENTITY
    "Hi there!",
    "Who are you?",
    "What is your name?",
    "Are you a robot?",
    "Good morning!",
    
    # SALES & INTERACTIVITY (HUNGER/CRONTROL)
    "I am hungry",
    "Suggest me something to eat",
    "I want some tasty food",
    "I am famished, what should I get?",
    "What's the best thing on your menu?",
    "Tell me about your signature dishes",
    "I'm in a hurry, what's quick?",
    "I want something spicy and rich",
    "Can you paint a picture of your best meal?",
    "Why should I eat at IYI Dining?",
    
    # BUDGET & GROUP SIZE
    "We are a group of 4, what do you recommend?",
    "I have a budget of 20 pounds, what can I get?",
    "Group of 6 people, budget 50. Suggest something.",
    "I only have 10 pounds, can I eat something good?",
    "We want a big family feast, what do you have?",
    
    # SPECIFIC MENU QUERIES
    "What is Ranjha Gosht?",
    "Tell me about Lamb Kebab Barg",
    "Do you have Baklava?",
    "How much is the Turkish Tea?",
    "Is the Chicken Adana Kebab spicy?",
    "Tell me about your hummus options",
    "What's in the Bannu Pulao?",
    "Do you have any seafood?",
    "Tell me about your desserts",
    "What drinks do you have?",
    
    # GADGETS & OUT OF SCOPE
    "I want to buy an iPhone",
    "Do you sell Samsung tablets?",
    "What is the weather like in London today?",
    "Who is the president of the US?",
    "Can you help me with some python code?",
    "What is the capital of France?",
    "Tell me a joke",
    "2 + 2 = ?",
    "What's the stock price of Apple?",
    "Do you have pizza?",
    "I want some sushi please",
    "Can I get a burger here?",
    "Do you serve alcohol?",
    "Can I get a laptop from you?",
    
    # RESERVATIONS & LOCATION
    "Where are you located?",
    "How can I book a table?",
    "What's your phone number?",
    "Are you open right now?",
    "Give me your address",
    
    # CART & ORDERING
    "Add Lamb Kebab Barg to my order",
    "I want to add Baklava to my cart",
    "How do I checkout?",
    "Can I pay with credit card?",
    "Remove the tea from my cart"
]

async def run_test():
    async with httpx.AsyncClient(timeout=180.0) as client:
        results = []
        print(f"Starting 50-prompt test (Actual: {len(PROMPTS)})...")
        for i, prompt in enumerate(PROMPTS):
            print(f"Progress: {i+1}/{len(PROMPTS)}")
            try:
                res = await client.post("http://127.0.0.1:8002/chat", json={
                    "message": prompt,
                    "user_id": "comprehensive_test_user"
                })
                full_text = ""
                # Handle streaming or non-streaming
                if res.status_code == 200:
                    async for chunk in res.aiter_text():
                        full_text += chunk
                else:
                    full_text = f"ERROR: {res.status_code}"
                
                # Strip out the |AUDIO_URL|...|TEXT| part if needed for the core report
                display_text = full_text
                if "|TEXT|" in full_text:
                    display_text = full_text.split("|TEXT|")[-1]
                
                results.append({"prompt": prompt, "response": display_text.strip()})
            except Exception as e:
                results.append({"prompt": prompt, "response": f"FAILED: {e}"})
        
        with open("comprehensive_report.json", "w") as f:
            json.dump(results, f, indent=2)
        print("Test complete. Results saved to comprehensive_report.json")

if __name__ == "__main__":
    asyncio.run(run_test())
