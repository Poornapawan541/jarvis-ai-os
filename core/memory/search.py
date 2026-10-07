"""
=========================================
JARVIS MEMORY SEARCH
=========================================
"""


class MemorySearch:

    STOP_WORDS = {
        "what", "is", "my", "the", "a", "an",
        "of", "to", "and", "in", "on", "for",
        "do", "does", "did", "i", "me", "you",
        "your", "this", "that"
    }

    def search(self, memories, query, limit=10):
        """
        Return the most relevant memories using keyword matching.
        """

        query_words = {
            word.strip(".,!?")
            for word in query.lower().split()
            if word.strip(".,!?") not in self.STOP_WORDS
        }

        scored = []

        for memory in memories:

            memory_words = {
                word.strip(".,!?")
                for word in memory.lower().split()
                if word.strip(".,!?") not in self.STOP_WORDS
            }

            score = len(query_words & memory_words)

            scored.append((score, memory))

        scored.sort(key=lambda item: item[0], reverse=True)

        results = []

        for score, memory in scored:

            if score > 0:
                results.append(memory)

            if len(results) >= limit:
                break

        return results


memory_search = MemorySearch()