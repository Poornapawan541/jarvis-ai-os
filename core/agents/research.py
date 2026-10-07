"""
=========================================
JARVIS RESEARCH AGENT
=========================================
"""

from core.browser.actions import browser_actions
from core.services.logger import logger


class ResearchAgent:

    name = "research"

    SEARCH_PREFIXES = (
        "search ",
        "google ",
        "look up ",
        "find information about ",
        "research ",
    )

    def can_handle(self, text):

        text = text.lower().strip()

        # Only activate when the user explicitly
        # asks Jarvis to perform a search.
        return text.startswith(self.SEARCH_PREFIXES)

    def execute(self, text):

        text = text.strip()

        logger.info(
            f"Researching: {text}"
        )

        # Remove command prefix
        query = text

        for prefix in self.SEARCH_PREFIXES:

            if text.lower().startswith(prefix):

                query = text[len(prefix):].strip()

                break

        if not query:
            return "What would you like me to search for?"

        browser_actions.search_google(query)

        return (
            f"I searched Google for '{query}'."
        )


research_agent = ResearchAgent()