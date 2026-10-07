"""
=========================================
JARVIS COMMAND NORMALIZER
=========================================

Converts natural language into a normalized
command format for the Planner.

Example:

Input:
Open Chrome, then GitHub afterwards search AI.

Output:
open chrome and open github and search ai
"""

import re


class CommandNormalizer:

    def __init__(self):

        # Different ways users separate commands
        self.connectors = {
            " and then ": " and ",
            " then ": " and ",
            " after that ": " and ",
            " afterwards ": " and ",
            " next ": " and ",
            " finally ": " and ",
            " also ": " and ",
        }

        # Different verbs users may use
        self.verbs = {
            "launch": "open",
            "start": "open",
            "run": "open",

            "find": "search",
            "look up": "search",
            "lookup": "search",

            "calculate": "calculate",
        }
        # Common polite command prefixes
        self.prefixes = [
            "please ",
            "can you ",
            "could you ",
            "would you ",
            "will you ",
        ]
    def normalize(self, text: str) -> str:

        text = text.lower().strip()

        # -----------------------------
        # Remove polite prefixes
        # -----------------------------
        for prefix in self.prefixes:
            if text.startswith(prefix):
                text = text[len(prefix):]
                break

        # -----------------------------
        # Remove punctuation
        # -----------------------------
        text = re.sub(r"[.,!?;:]", " ", text)

        # -----------------------------
        # Normalize connectors
        # -----------------------------
        padded = f" {text} "

        for old, new in self.connectors.items():
            padded = padded.replace(old, new)

        text = padded.strip()

        # -----------------------------
        # Normalize verbs
        # -----------------------------
        for old, new in self.verbs.items():

            if text.startswith(old):

                text = text.replace(
                    old,
                    new,
                    1,
                )

        # -----------------------------
        # Remove duplicate spaces
        # -----------------------------
        text = " ".join(text.split())

        return text


normalizer = CommandNormalizer()