import sys
import os
import asyncio

# Add scripts to path
sys.path.append(os.path.join(os.getcwd(), 'model_training', 'scripts'))

import router
from streaming_engine import StreamingEngine
from rag_engine import RAGEngine
from phi_handler import PhiHandler
from llama_handler import LlamaHandler
from memory_manager import MemoryManager
import hardcode_rules as rules

async def test_refinements():
    # Mock context
    OLLAMA_HOST = "http://localhost:11434"
    MENU_JSON = "model_training/data/menu.json"
    EXAMPLES_TXT = "model_training/data/sales_examples_new.txt"
    
    # 1. Test Router
    print("--- Testing Router ---")
    prompts = [
        "give us some recommendations",
        "what is your budget options?",
        "recommend some cheap food",
        "recommendations for 4 people"
    ]
    for p in prompts:
        intent = router.classify_intent(p)
        print(f"Prompt: '{p}' -> Intent: {intent}")
    
    # 2. Test Engine Fallback (Mocked handlers)
    print("\n--- Testing Engine Fallback ---")
    # We won't fully init RAG for a quick test, just check the logic flow
    # This part requires a bit of setup if we want to run it end-to-end
    # For now, let's just verify the router which was the main failure point for "recommendations"
    
if __name__ == "__main__":
    asyncio.run(test_refinements())
