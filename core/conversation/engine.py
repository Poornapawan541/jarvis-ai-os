"""
=========================================
JARVIS CONVERSATION ENGINE
=========================================
"""

from core.memory.manager import MemoryManager
from core.brain.prompts import prompt_builder
from core.brain.llm import llm
from core.conversation.history import history
from core.skills.router import router
from core.services.logger import logger


class ConversationEngine:

    def __init__(self):
        self.memory = MemoryManager()
    

    

    def reply(self, user_input):

        logger.info(f"User: {user_input}")

        # Save memory
        self.memory.remember(user_input)
        logger.info("Memory processed")

        # Search memory
        memories = self.memory.search_memories(user_input)
        logger.info(f"Retrieved {len(memories)} memories")

        # Store conversation
        history.add("user", user_input)

        # Try local skills
        skill_response = router.route(user_input)

        if skill_response is not None:
            logger.info("Skill Router handled the request")
            history.add("assistant", skill_response)
            return skill_response

        # Build prompt
        prompt = prompt_builder.build(
            user_input=user_input,
            memories=memories,
        )

        logger.info("Sending prompt to Llama 3")

    # Ask LLM
        answer = llm.ask(prompt)

        logger.info("LLM response received")

        history.add("assistant", answer)

        return answer
    def close(self):
        self.memory.close()


engine = ConversationEngine()