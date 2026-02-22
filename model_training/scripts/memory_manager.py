from langchain_classic.memory import ConversationBufferMemory
from typing import Dict

class SessionMemory:
    def __init__(self):
        self.memory = ConversationBufferMemory(return_messages=True)
        
    def add_user_message(self, message: str):
        self.memory.chat_memory.add_user_message(message)
        
    def add_ai_message(self, message: str):
        self.memory.chat_memory.add_ai_message(message)
        
    def get_history(self, limit: int = 10):
        # We extract history for the raw model prompts
        messages = self.memory.chat_memory.messages[-limit:]
        formatted = []
        for m in messages:
            # Simple role mapping for the raw chat calls
            role = "user" if m.type == "human" else "assistant"
            formatted.append({"role": role, "content": m.content})
        return formatted

class MemoryManager:
    def __init__(self):
        self.sessions: Dict[str, SessionMemory] = {}

    def get_session(self, user_id: str) -> SessionMemory:
        if user_id not in self.sessions:
            self.sessions[user_id] = SessionMemory()
        return self.sessions[user_id]
