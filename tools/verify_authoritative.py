import asyncio
import sys
import os
import json

# Add scripts to path
sys.path.append(os.path.join(os.getcwd(), "model_training/scripts"))

from streaming_engine import StreamingEngine
from rag_engine import RAGEngine
from phi_handler import PhiHandler
from llama_handler import LlamaHandler
from memory_manager import MemoryManager
import order_db

async def test_authoritative_flow():
    print("Testing Authoritative Hybrid Flow...")
    
    # Initialize components
    OLLAMA_HOST = "http://127.0.0.1:11434"
    DATA_DIR = "model_training/data"
    
    # Initialize DB
    order_db.init_db()
    
    # Pre-seed an order for "test_user_2" to test intelligence
    order_db.save_order("test_user_2", ["Prawns Tikka"])
    
    rag = RAGEngine(
        menu_path=os.path.join(DATA_DIR, "menu.json"),
        examples_path=os.path.join(DATA_DIR, "sales_examples_new.txt"),
        ollama_url=OLLAMA_HOST,
        embed_model="nomic-embed-text"
    )
    
    # We need real menu data for the fallback to work
    with open(os.path.join(DATA_DIR, "menu.json"), "r") as f:
        menu_data = json.load(f)
    
    memory = MemoryManager()
    phi = PhiHandler(OLLAMA_HOST, "phi3:mini", menu_data)
    llama = LlamaHandler(OLLAMA_HOST, "llama3.2:1b", menu_data)
    
    engine = StreamingEngine(rag, memory, phi, llama)
    
    test_cases = [
        ("test_user_1", "how are you"),                # HARDCODED Identity
        ("test_user_1", "show me starters"),           # HARDCODED Menu Category
        ("test_user_1", "how do I book a table?"),     # HARDCODED Reservation
        ("test_user_1", "what is the price of baked meat?"), # PHI3 Factual
        ("test_user_1", "tell me about prawns tikka"), # PHI3 Factual
        ("test_user_2", "i am hungry, what do you suggest?"), # LLAMA_RAG + Order Intelligence
        ("test_user_2", "anything else?"),             # LLAMA_RAG + Memory
    ]
    
    for uid, q in test_cases:
        print(f"\n[{uid}] User: {q}")
        print("Aureeq: ", end="", flush=True)
        async for chunk in engine.generate_response(uid, q):
            print(chunk, end="", flush=True)
        print("\n" + "-"*50)

if __name__ == "__main__":
    asyncio.run(test_authoritative_flow())
