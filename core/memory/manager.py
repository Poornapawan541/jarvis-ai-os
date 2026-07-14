"""
=========================================
JARVIS MEMORY MANAGER
=========================================
"""

from core.memory.database import MemoryDatabase
from core.memory.search import memory_search
from core.services.logger import logger

class MemoryManager:

    def __init__(self):
        self.db = MemoryDatabase()
        logger.info("Memory Manager initialized")

    def should_remember(self, text):

        keywords = [
            "my name is",
            "i am",
            "i like",
            "i love",
            "my birthday",
            "my email",
            "remember",
            "favorite",
            "prefer",
        ]

        text = text.lower()

        return any(keyword in text for keyword in keywords)

    def remember(self, text):

        if self.should_remember(text):
            self.db.save_memory(text)
            logger.info(f"Memory saved: {text}")
        else:
            logger.info("Input not important enough to store")

    def close(self):
        self.db.close()
        logger.info("Memory database closed")

        
    def search_memories(self, query):
        memories = self.db.get_all_memories()

        logger.info(
            f"Searching {len(memories)} stored memories"
        )

        results = memory_search.search(
            memories,
            query
        )

        logger.info(
            f"Found {len(results)} matching memories"
        )

        return results