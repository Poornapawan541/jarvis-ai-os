"""
=========================================
JARVIS AI - Ollama HTTP Client
=========================================
"""

import requests

from core.services.logger import logger


class LLM:

    def __init__(self):

        self.url = "http://127.0.0.1:11434/api/chat"
        self.model = "llama3:latest"

        # Reuse HTTP connection
        self.session = requests.Session()

        # Keep model loaded in Ollama
        self.keep_alive = "10m"

        # Avoid hanging forever
        self.timeout = 60

    def ask(self, prompt: str) -> str:

        payload = {
            "model": self.model,

            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Jarvis, a helpful AI assistant. "
                        "Answer briefly, naturally and clearly."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            "stream": False,

            # Keep Llama loaded between requests
            "keep_alive": self.keep_alive,

            # Reduce unnecessary generation
            "options": {
                "temperature": 0.3,
                "num_predict": 256
            }
        }

        try:

            logger.info("Sending request to Ollama")

            response = self.session.post(
                self.url,
                json=payload,
                timeout=self.timeout
            )

            response.raise_for_status()

            data = response.json()

            answer = data["message"]["content"].strip()

            logger.info("LLM response received")

            return answer

        except requests.exceptions.ConnectionError:

            logger.error(
                "Ollama is not running. Start it with: ollama serve"
            )

            return (
                "Ollama is not running. "
                "Please start Ollama first."
            )

        except requests.exceptions.Timeout:

            logger.error("LLM request timed out")

            return "Sorry, the response took too long."

        except Exception as e:

            logger.error(f"LLM error: {e}")

            return "Sorry, I couldn't process that request."


llm = LLM()