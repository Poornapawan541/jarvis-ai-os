"""
=========================================
JARVIS CONVERSATION ENGINE
=========================================
"""

from core.memory.manager import MemoryManager

from core.brain.prompts import prompt_builder
from core.brain.llm import llm

from core.conversation.history import history
from core.conversation.resolver import resolver

from core.agents.router import router as agent_router
from core.skills.router import router as skill_router

from core.planner.planner import planner
from core.planner.executor import executor

from core.services.logger import logger


class ConversationEngine:

    def __init__(self):

        self.memory = MemoryManager()
    def get_conversation_context(self, count=5):
        messages = history.get_recent(count)

        if not messages:
            return ""

        context = []

        for message in messages:
            role = message["role"].capitalize()
            content = message["content"]
            context.append(f"{role}: {content}")

        return "\n".join(context)

    
    # =====================================
    # FAST COMMAND DETECTION
    # =====================================

    def quick_response(self, text):

        text = text.lower().strip()

        responses = {

            "hello":
                "Hello Pawan. How can I help you?",

            "hi":
                "Hello Pawan. How can I help you?",

            "hey":
                "Hey Pawan. What can I do for you?",

            "hello jarvis":
                "Hello Pawan. I am listening.",

            "hi jarvis":
                "Hello Pawan. How can I help?",

            "hey jarvis":
                "Yes Pawan. I'm listening.",

            "good morning":
                "Good morning Pawan.",

            "good afternoon":
                "Good afternoon Pawan.",

            "good evening":
                "Good evening Pawan.",

            "thanks":
                "You're welcome, Pawan.",

            "thank you":
                "You're welcome, Pawan.",
        }

        return responses.get(text)

    # =====================================
    # EXIT COMMAND
    # =====================================

    def is_exit_command(self, text):

        text = text.lower().strip()

        exit_commands = {
            "exit",
            "quit",
            "bye",
            "goodbye",
            "stop",
            "shutdown",
        }

        return text in exit_commands

    # =====================================
    # MAIN REPLY
    # =====================================

    def reply(self, user_input):

        user_input = user_input.strip()

                # Resolve simple follow-up search commands
        user_input = resolver.resolve(user_input)

        logger.info(
            f"User: {user_input}"
        )

        # =================================
        # FAST RESPONSE
        # =================================

        quick = self.quick_response(
            user_input
        )

        if quick:

            logger.info(
                "⚡ Quick response detected. "
                "Skipping memory, agents, planner and LLM."
            )

            history.add(
                "user",
                user_input,
            )

            history.add(
                "assistant",
                quick,
            )

            return quick

        # =================================
        # EXIT
        # =================================

        if self.is_exit_command(user_input):

            logger.info(
                "🛑 Exit command detected."
            )

            answer = "Goodbye Pawan."

            history.add(
                "user",
                user_input,
            )

            history.add(
                "assistant",
                answer,
            )

            return answer

        # =================================
        # MEMORY
        # =================================

        self.memory.remember(
            user_input
        )

        logger.info(
            "Memory processed"
        )

        memories = self.memory.search_memories(
            user_input
        )

        logger.info(
            f"Retrieved {len(memories)} memories"
        )

        history.add(
            "user",
            user_input,
        )

        # =================================
        # AGENT ROUTER
        # =================================

        logger.info(
            "Routing request to an agent"
        )

        agent = agent_router.route(
            user_input
        )

        if agent:

            logger.info(
                f"Agent '{agent.name}' handling request"
            )

            try:

                answer = agent.execute(
                    user_input
                )

                if answer:

                    history.add(
                        "assistant",
                        answer,
                    )

                    return answer

            except Exception as e:

                logger.error(
                    f"Agent '{agent.name}' failed: {e}"
                )

        # =================================
        # SKILL ROUTER
        # =================================

        logger.info(
            "Routing request to a skill"
        )

        try:

            skill_result = skill_router.route(
                user_input
            )

            if skill_result:

                logger.info(
                    "Skill successfully handled request"
                )

                history.add(
                    "assistant",
                    skill_result,
                )

                return skill_result

        except Exception as e:

            logger.error(
                f"Skill routing failed: {e}"
            )

        # =================================
        # PLANNER
        # =================================

        logger.info(
            "Creating execution plan"
        )

        tasks = planner.create_plan(
            user_input
        )

        logger.info(
            f"Planner created {len(tasks)} task(s)"
        )

        # =================================
        # EXECUTOR
        # =================================

        if tasks:

            logger.info(
                "Executing plan"
            )

            results = executor.execute(
                tasks
            )

            completed = results["completed"]
            failed = results["failed"]

            logger.info(
                f"Execution finished. "
                f"Completed={len(completed)}, "
                f"Failed={len(failed)}"
            )

            # -----------------------------
            # Completed tasks
            # -----------------------------

            if completed:

                replies = []

                for task in completed:

                    logger.info(
                        f"Task completed: "
                        f"{task.action}"
                    )

                    if task.result:

                        replies.append(
                            str(task.result)
                        )

                if replies:

                    answer = "\n".join(
                        replies
                    )

                    history.add(
                        "assistant",
                        answer,
                    )

                    return answer

            # -----------------------------
            # Failed tasks
            # -----------------------------

            for task in failed:

                logger.warning(
                    f"Task failed: "
                    f"{task.action} -> "
                    f"{task.result}"
                )

        # =================================
        # LLM FALLBACK
        # =================================

        logger.info(
            "No executable command. "
            "Using LLM."
        )

        prompt = prompt_builder.build(
            user_input=user_input,
            memories=memories,
        )

        logger.info(
            "Sending prompt to Llama 3"
        )

        answer = llm.ask(
            prompt
        )

        logger.info(
            "LLM response received"
        )

        history.add(
            "assistant",
            answer,
        )

        return answer

    # =====================================
    # CLOSE
    # =====================================

    def close(self):

        self.memory.close()


engine = ConversationEngine()