import asyncio
import os
import sys

# Add current dir to path
sys.path.append(os.path.dirname(__file__))

from rag_engine import RAGEngine

OLLAMA_HOST_URL = "http://127.0.0.1:11434"
MODEL_EMBED = "nomic-embed-text"
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
MENU_JSON_PATH = os.path.join(DATA_DIR, "menu.json")
EXAMPLES_TXT_PATH = os.path.join(DATA_DIR, "sales_examples_new.txt")

async def test():
    rag = RAGEngine(MENU_JSON_PATH, EXAMPLES_TXT_PATH, OLLAMA_HOST_URL, MODEL_EMBED)
    await rag.init_menu()
    
    query = "what do you offer in seafood"
    print(f"\nQuery: {query}")
    results = await rag.search_menu(query, k=6)
    
    print("\nSearch Results:")
    for i, item in enumerate(results):
        print(f"{i+1}. {item['name']} ({item['category']}) - {item.get('price', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(test())
