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

    async def translate(self, text: str, target_lang: str) -> str:
        prompt = f"Translate the following text to {target_lang}. Return ONLY the direct translation, nothing else, no quotes, no markdown:\n\n{text}"
        messages = [{"role": "user", "content": prompt}]
        
        full_trans = ""
        try:
            resp = await self.http_client.post(f"{self.ollama_url}/api/chat", json={
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": { "temperature": 0.0 }
            })
            resp_data = resp.json()
            full_trans = resp_data.get("message", {}).get("content", "").strip()
        except Exception as e:
            print(f"Translation error: {e}")
        return full_trans or text

    async def handle(self, query: str, history: List[Dict], menu_context: List[Dict], style_example: str, order_history_context: str, is_gadget_query: bool = False, language: str = "en") -> str:
        # Construct menu string for Llama context
        menu_list = ""
        for item in menu_context:
            price = item.get('price', '0.00')
            if "baked meat" in item.get('name', '').lower(): price = "94.99"
            # Include ID for robust internal matching
            menu_list += f"- {item['name']} (ID: {item['id']}, Price: £{price}): {item.get('description', '')}\n"

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

        if language == 'ar':
            system_prompt += "\n\nCRITICAL INSTRUCTION: You MUST write your ultimate response entirely in Arabic. The user's input might be in English or Arabic, but your answer to them MUST be in Arabic. \n\nIMPORTANT FOR IMAGE MATCHING: When mentioning specific dishes, always include their tag like this: [ID: item_id]. This allows the system to show the correct picture. You should also keep the English name in brackets if it helps the user. Example: 'أقترح عليك تجربة كباب شيش الدجاج (Chicken Shish Kebab) [ID: chicken_shish_kebab]'."

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
            print(f"Llama Handler Error: {e}", flush=True)
            traceback.print_exc()
            raise e
