"""
=========================================
JARVIS COMMAND PARSER
=========================================
"""

import re

from core.planner.normalizer import normalizer


class CommandParser:
    """
    Converts natural language into individual
    normalized commands for the planner.
    """

    COMMAND_STARTS = (
        "open ",
        "close ",
        "search ",
        "calculate ",
        "find ",
        "look up ",
    )

    def parse(self, text: str) -> list[str]:

        # Normalize the complete sentence first
        text = normalizer.normalize(text)

        # Find real command boundaries.
        # "and" is treated as a separator only when
        # the following text starts another command.
        pattern = r"\s+and\s+(?=(?:open|close|search|calculate|find|look up)\b)"

        commands = re.split(pattern, text)

        return [
            command.strip()
            for command in commands
            if command.strip()
        ]


parser = CommandParser()