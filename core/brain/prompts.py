"""
=========================================
JARVIS PROMPT BUILDER
=========================================
"""


class PromptBuilder:

    def build(self, user_input, memories=None):

        if memories is None:
            memories = []

        memory_block = ""

        if memories:

            memory_block = "Known information about the user:\n"

            for memory in memories:
                memory_block += f"- {memory}\n"

            memory_block += "\n"

        prompt = f"""
You are Jarvis, an intelligent, professional and friendly AI assistant.

{memory_block}
User:
{user_input}

Jarvis:
"""

        return prompt.strip()


prompt_builder = PromptBuilder()