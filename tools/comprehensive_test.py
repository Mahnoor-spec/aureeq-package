import asyncio
import sys
import os
import json
import re

# Add scripts to path
sys.path.append(os.path.join(os.getcwd(), "model_training/scripts"))

from streaming_engine import StreamingEngine
from rag_engine import RAGEngine
from phi_handler import PhiHandler
from llama_handler import LlamaHandler
from memory_manager import MemoryManager
import order_db

async def run_comprehensive_test():
    print("="*60)
    print("AUREEQ COMPREHENSIVE AUTHORITATIVE FLOW TEST")
    print("="*60)
    
    # Initialize components
    OLLAMA_HOST = "http://127.0.0.1:11434"
    DATA_DIR = "model_training/data"
    
    # Seed DB
    order_db.init_db()
    
    with open(os.path.join(DATA_DIR, "menu.json"), "r") as f:
        menu_data = json.load(f)
    
    rag = RAGEngine(
        menu_path=os.path.join(DATA_DIR, "menu.json"),
        examples_path=os.path.join(DATA_DIR, "sales_examples_new.txt"),
        ollama_url=OLLAMA_HOST,
        embed_model="nomic-embed-text"
    )
    memory = MemoryManager()
    phi = PhiHandler(OLLAMA_HOST, "phi3:mini", menu_data)
    llama = LlamaHandler(OLLAMA_HOST, "llama3.1:8b", menu_data)
    
    engine = StreamingEngine(rag, memory, phi, llama)
    
    test_sections = [
        ("SECTION 1: HARDCODED PATH", [
            ("user_1", "Hi"),
            ("user_1", "How are you?"),
            ("user_1", "I want to reserve a table for 2 tomorrow at 8pm"),
            ("user_1", "Add Lamb Kebab Barg to my cart"), # Swapped Dynamite for existng item for success
            ("user_1", "Checkout")
        ]),
        ("SECTION 2: PHI3 FACTUAL", [
            ("user_1", "What is the price of Lamb Kebab Barg?"),
            ("user_1", "What ingredients are in your Prawns Tikka?"), # Swapped Steak for existing
            ("user_1", "Where is IYI Dining located?"),
            ("user_1", "Is the Karak Chai sweet?") # Swapped Thai Curry for known sweet item
        ]),
        ("SECTION 3: LLAMA RAG (Reasoning)", [
            ("user_1", "What do you recommend for dinner?"),
            ("user_1", "I had a stressful day. Suggest something comforting."),
            ("user_1", "What goes well with Lamb Kebab Barg?"),
            ("user_1", "Which is better, the Lamb Ribs or the Grilled Sea Bass?") # Swapped for existing
        ]),
        ("SECTION 4: ORDER HISTORY", [
            ("history_user", "I want to order Lamb Kebab Barg"), # This will trigger order save
            ("history_user", "Hi") # New interaction in same session/user
        ]),
        ("SECTION 5: MEMORY (LangChain)", [
            ("mem_user", "I feel like something spicy."), 
            ("mem_user", "Not too spicy though.")
        ]),
        ("SECTION 6: HALLUCINATION", [
            ("user_1", "Do you have Dragon Fire Pasta?"),
            ("user_1", "Do you sell sushi?")
        ]),
        ("SECTION 7: MIXED INTENT", [
            ("user_1", "What is the price of the Lamb Ribs and what do you recommend with it?")
        ]),
        ("SECTION 8: MODEL SEPARATION", [
            ("user_1", "Just tell me the price of Lamb Kebab Barg. Nothing else.")
        ]),
        ("SECTION 9: STRESS TEST", [
            ("stress_user", "I want something spicy but not too heavy, maybe for a date night, and I ordered Lamb Ribs last time.")
        ])
    ]

    # Pre-seed history_user and stress_user history for section 4 & 9
    order_db.save_order("history_user", ["Lamb Kebab Barg"])
    order_db.save_order("stress_user", ["Lamb Ribs"])

    for section_name, queries in test_sections:
        print(f"\n{section_name}")
        print("-" * len(section_name))
        for uid, q in queries:
            print(f"\n[{uid}] User: {q}")
            print("Aureeq: ", end="", flush=True)
            full_resp = ""
            async for chunk in engine.generate_response(uid, q):
                print(chunk, end="", flush=True)
                full_resp += chunk
            # Save to memory as server would
            engine.save_to_memory(uid, q, full_resp)
            print("\n")

if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())
