"""
=========================================
JARVIS MEMORY SEARCH
=========================================
"""


class MemorySearch:

    def search(self, memories, query, limit=3):
        """
        Return the most relevant memories using simple keyword matching.
        """

        query_words = set(query.lower().split())

        scored = []

        for memory in memories:

            score = 0

            memory_words = set(memory.lower().split())

            score = len(query_words & memory_words)

            scored.append((score, memory))

        scored.sort(reverse=True)

        results = []

        for score, memory in scored:

            if score > 0:
                results.append(memory)

            if len(results) >= limit:
                break

        return results


memory_search = MemorySearch()