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

        text = text.lower().strip()

        # Questions should never be stored as memories
        question_starts = [
            "what",
            "who",
            "where",
            "when",
            "why",
            "how",
            "do you",
            "did you",
            "can you",
            "could you",
            "would you",
            "or do you",
        ]

        if any(text.startswith(question) for question in question_starts):
            return False

        keywords = [
            "my name is",
            "i am",
            "i like",
            "i love",
            "my birthday",
            "my email",
            "remember that",
            "remember my",
            "i prefer",
        ]

        return (
            any(keyword in text for keyword in keywords)
            or (
                "my favorite " in text
                and " is " in text
            )
        )
    def find_favorite_memory(self, text):

        text = text.lower()

        if "my favorite " not in text:
            return None

        start = text.find("my favorite ") + len("my favorite ")
        remainder = text[start:]

        if " is " not in remainder:
            return None

        category = remainder.split(" is ", 1)[0].strip()

        memories = self.db.get_all_memories()

        for memory in memories:
            memory_lower = memory.lower()

            if f"my favorite {category}" in memory_lower:
                return memory

        return None
    def remember(self, text):

        if not self.should_remember(text):
            logger.info("Input not important enough to store")
            return

        old_memory = self.find_favorite_memory(text)

        if old_memory:
            updated = self.db.update_memory(old_memory, text)

            if updated:
                logger.info(
                    f"Memory updated: {old_memory} -> {text}"
                )
                return

        self.db.save_memory(text)
        logger.info(f"Memory saved: {text}")

    def close(self):
        self.db.close()
        logger.info("Memory database closed")

        
    def search_memories(self, query):

        memories = self.db.get_all_memories()

        logger.info(
            f"Searching {len(memories)} stored memories"
        )

        query_lower = query.lower().strip()

        # For a specific favorite category,
        # return only that category's memory.
        if "favorite " in query_lower:

            start = query_lower.find("favorite ") + len("favorite ")
            category = query_lower[start:].split("?", 1)[0].strip()

            if category and "things" not in category and "thing" not in category:

                category_words = category.split()

                for memory in memories:
                    memory_lower = memory.lower()

                    if "my favorite " not in memory_lower:
                        continue

                    memory_start = (
                        memory_lower.find("my favorite ")
                        + len("my favorite ")
                    )

                    memory_category = (
                        memory_lower[memory_start:]
                        .split(" is ", 1)[0]
                        .strip()
                    )

                    if memory_category == category:
                        logger.info(
                            f"Found specific favorite memory: {memory}"
                        )
                        return [memory]

        results = memory_search.search(
            memories,
            query
        )

        logger.info(
            f"Found {len(results)} matching memories"
        )

        return results