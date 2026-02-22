import json
import httpx
import traceback
import random
from typing import List, Dict, Optional
import hardcode_rules as rules

class LlamaHandler:
    def __init__(self, ollama_url: str, model: str, menu_data: List[Dict]):
        self.ollama_url = ollama_url
        self.model = model
        self.menu_data = menu_data
        # Disable proxies to avoid localhost connection issues
        self.http_client = httpx.AsyncClient(timeout=300.0, trust_env=False)

    async def handle(self, query: str, history: List[Dict], menu_context: List[Dict], style_example: str, order_history_context: str, is_gadget_query: bool = False) -> str:
        # Construct menu string for Llama context
        menu_list = ""
        for item in menu_context:
            price = item.get('price', '0.00')
            # Fix pricing for baked meat if needed (special case from previous code)
            if "baked meat" in item.get('name', '').lower(): price = "94.99"
            menu_list += f"- {item['name']} (£{price}): {item.get('description', '')}\n"

        if is_gadget_query:
            # For gadgets, we use the template from rules if defined, or a simplified one here.
            gadget_name = query # simple approximation
            system_prompt = rules.SYSTEM_PROMPT_OPENAI.format(
                global_context=f"The user is asking about {gadget_name}. Politely pivot to food.",
                style_example="",
                context_item=f"AVAILABLE MENU:\n{menu_list}"
            )
        else:
            system_prompt = rules.SYSTEM_PROMPT_OPENAI.format(
                global_context=f"AVAILABLE MENU (STRICT GROUNDING):\n{menu_list}",
                style_example=f"STYLE RULES: Precise, confident, upsell, and polite. Not too lengthy.",
                context_item=f"USER HISTORY/CONTEXT:\n{order_history_context}"
            )

        messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": query}]
        print(f"DEBUG LLAMA PROMPT: {system_prompt[:250]}...", flush=True)

        try:
             async with self.http_client.stream("POST", f"{self.ollama_url}/api/chat", json={
                "model": self.model,
                "messages": messages,
                "stream": True,
                "options": {
                    "temperature": 0.0,
                    "stop": ["User:", "Aureeq:", "System:"]
                }
            }) as resp:
                async for line in resp.aiter_lines():
                    if not line: continue
                    chunk = json.loads(line)
                    content = chunk.get("message", {}).get("content", "")
                    if content:
                        clean_content = content.replace("*", "").replace("#", "")
                        if clean_content: yield clean_content
        except Exception as e:
            print(f"Llama Handler Error: {e}")
            traceback.print_exc()
            raise e
