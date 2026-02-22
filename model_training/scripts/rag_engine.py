import json
import os
import re
import numpy as np
import httpx
from typing import List, Dict, Optional, Tuple

class RAGEngine:
    def __init__(self, menu_path: str, examples_path: str, ollama_url: str, embed_model: str):
        self.menu_path = menu_path
        self.examples_path = examples_path
        self.ollama_url = ollama_url
        self.embed_model = embed_model
        
        self.menu_data: List[Dict] = []
        self.menu_vectors: Optional[np.ndarray] = None
        
        self.example_data: List[Tuple[str, str]] = [] # (User, Agent)
        self.example_vectors: Optional[np.ndarray] = None
        
        # Disable proxies for embeddings
        self.client = httpx.AsyncClient(timeout=60.0, trust_env=False)

    async def get_embedding(self, text: str) -> np.ndarray:
        # nomic-embed-text is 768, but we should detect first valid size
        target_dim = getattr(self, "target_dim", 768) 
        try:
            resp = await self.client.post(f"{self.ollama_url}/api/embeddings", json={
                "model": self.embed_model,
                "prompt": text
            })
            if resp.status_code != 200:
                print(f"Embedding Error {resp.status_code}: {resp.text}")
                return np.zeros(target_dim)
            
            data = resp.json()
            vec = np.array(data["embedding"])
            if not hasattr(self, "target_dim"):
                self.target_dim = vec.shape[0]
            return vec
        except Exception as e:
            print(f"Embedding Exception: {e}")
            return np.zeros(target_dim)

    async def init_menu(self):
        print("Loading Menu...")
        try:
            if not os.path.exists(self.menu_path):
                print(f"Menu file missing: {self.menu_path}")
                return

            with open(self.menu_path, "r", encoding="utf-8") as f:
                self.menu_data = json.load(f)
            
            # Create embeddings for menu items (Name + Description + Tags)
            vectors = []
            for item in self.menu_data:
                text = f"{item['name']} {item['category']} {item.get('description', '')} {' '.join(item.get('tags', []))}"
                vec = await self.get_embedding(text)
                vectors.append(vec)
            
            if vectors:
                # Ensure all vectors have the same shape before array conversion
                v_shapes = [v.shape for v in vectors]
                if len(set(v_shapes)) > 1:
                    print(f"WARNING: Inconsistent embedding shapes detected: {set(v_shapes)}. Padding/Truncating...")
                    max_dim = max(s[0] for s in v_shapes)
                    fixed_vectors = []
                    for v in vectors:
                         if v.shape[0] < max_dim:
                             fixed_vectors.append(np.pad(v, (0, max_dim - v.shape[0])))
                         else:
                             fixed_vectors.append(v[:max_dim])
                    self.menu_vectors = np.array(fixed_vectors)
                else:
                    self.menu_vectors = np.array(vectors)
            
            print(f"Menu Loaded: {len(self.menu_data)} items.")
        except Exception as e:
            print(f"Failed to load menu: {e}")
            traceback.print_exc()

    async def init_examples(self):
        print("Loading Examples...")
        try:
            if not os.path.exists(self.examples_path):
                print(f"Examples file missing: {self.examples_path}")
                return

            with open(self.examples_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Simple parsing of "User: ... Agent: ..." blocks
            blocks = content.split("---")
            for block in blocks:
                if "User:" in block and "Agent:" in block:
                    user_part = block.split("User:")[1].split("Agent:")[0].strip()
                    agent_part = block.split("Agent:")[1].strip()
                    self.example_data.append((user_part, agent_part))
            
            # Embed user queries
            vectors = []
            for user_q, _ in self.example_data:
                vec = await self.get_embedding(user_q)
                vectors.append(vec)
            
            if vectors:
                v_shapes = [v.shape for v in vectors]
                if len(set(v_shapes)) > 1:
                     print(f"WARNING: Inconsistent example shapes: {set(v_shapes)}. Normalizing...")
                     max_dim = max(s[0] for s in v_shapes)
                     fixed_vectors = []
                     for v in vectors:
                          if v.shape[0] < max_dim:
                               fixed_vectors.append(np.pad(v, (0, max_dim - v.shape[0])))
                          else:
                               fixed_vectors.append(v[:max_dim])
                     self.example_vectors = np.array(fixed_vectors)
                else:
                    self.example_vectors = np.array(vectors)

            print(f"Examples Loaded: {len(self.example_data)} examples.")
        except Exception as e:
            print(f"Failed to load examples: {e}")
            traceback.print_exc()

    async def search_menu(self, query: str, k: int = 5) -> List[Dict]:
        if self.menu_vectors is None or len(self.menu_data) == 0:
            return []
            
        query_vec = await self.get_embedding(query)
        if np.all(query_vec == 0): return []

        # Cosine Similarity
        # (A . B) / (|A| * |B|)
        # Assuming normalized? No, let's just do dot product for now or explicit cosine
        norm_q = np.linalg.norm(query_vec)
        
        scores = []
        for i, doc_vec in enumerate(self.menu_vectors):
            norm_d = np.linalg.norm(doc_vec)
            if norm_d == 0 or norm_q == 0:
                score = 0
            else:
                score = np.dot(query_vec, doc_vec) / (norm_q * norm_d)
            scores.append((score, self.menu_data[i]))
            
        scores.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scores[:k]]

    async def search_examples(self, query: str, k: int = 1) -> str:
        if self.example_vectors is None or len(self.example_data) == 0:
            return ""
            
        query_vec = await self.get_embedding(query)
        if np.all(query_vec == 0): return ""

        norm_q = np.linalg.norm(query_vec)
        scores = []
        for i, doc_vec in enumerate(self.example_vectors):
            norm_d = np.linalg.norm(doc_vec)
            if norm_d == 0 or norm_q == 0:
                score = 0
            else:
                score = np.dot(query_vec, doc_vec) / (norm_q * norm_d)
            scores.append((score, self.example_data[i][1])) # Return Agent response as style
            
        scores.sort(key=lambda x: x[0], reverse=True)
        # Combine top k styles? Or just best one?
        # Usually best one is enough to set tone
        return scores[0][1] if scores else ""
