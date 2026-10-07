"""
=========================================
JARVIS AGENT ROUTER
=========================================
"""

from core.agents.browser import browser_agent
from core.agents.research import research_agent

from core.services.logger import logger


class AgentRouter:

    def __init__(self):

        self.agents = [
            browser_agent,
            research_agent,
        ]

        logger.info(
            f"{len(self.agents)} agent(s) loaded."
        )

    def route(self, text):

        text = text.lower().strip()

        logger.info(
            f"Routing request: {text}"
        )

        for agent in self.agents:

            try:

                if agent.can_handle(text):

                    logger.info(
                        f"Selected agent: {agent.name}"
                    )

                    return agent

            except Exception as e:

                logger.error(
                    f"Agent '{agent.name}' "
                    f"routing failed: {e}"
                )

        logger.info(
            "No suitable agent found"
        )

        return None


router = AgentRouter()