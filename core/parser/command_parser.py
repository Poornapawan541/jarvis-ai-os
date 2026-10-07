"""
=========================================
JARVIS COMMAND PARSER
=========================================
"""

import re


class CommandParser:

    OPEN_WORDS = [
        "open",
        "launch",
        "start",
        "run",
    ]

    REMOVE_WORDS = [
        "please",
        "could",
        "can",
        "you",
        "my",
        "the",
    ]

    def normalize(self, text):

        text = text.lower().strip()

        # Remove punctuation
        text = re.sub(r"[^\w\s]", "", text)

        # Remove filler words
        words = [
            word
            for word in text.split()
            if word not in self.REMOVE_WORDS
        ]

        text = " ".join(words)

        return text


parser = CommandParser()