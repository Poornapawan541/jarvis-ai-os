"""
=========================================
JARVIS AI - Ollama HTTP Client
=========================================
"""

import requests


class LLM:
    def __init__(self):
        self.url = "http://127.0.0.1:11434/api/chat"
        self.model = "llama3:latest"

    def ask(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are Jarvis, a helpful AI assistant. Answer briefly and clearly."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }

        response = requests.post(self.url, json=payload)
        response.raise_for_status()

        return response.json()["message"]["content"]


llm = LLM()