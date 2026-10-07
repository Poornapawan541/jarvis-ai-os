"""
=========================================
JARVIS INTENT EXPANDER
=========================================

Expands incomplete commands by inheriting
the previous action.

Example

Input:
open chrome and github and vscode

Output:
[
    "open chrome",
    "open github",
    "open vscode"
]
"""


class IntentExpander:

    def __init__(self):

        self.actions = [
            "open",
            "close",
            "search",
            "calculate",
        ]

    def expand(self, text):

        parts = [
            part.strip()
            for part in text.split(" and ")
            if part.strip()
        ]

        expanded = []

        previous_action = None

        for part in parts:

            words = part.split()

            if not words:
                continue

            first = words[0]

            # -------------------------
            # New action
            # -------------------------
            if first in self.actions:

                previous_action = first

                expanded.append(part)

                continue

            # -------------------------
            # Missing action
            # -------------------------
            if previous_action:

                expanded.append(
                    f"{previous_action} {part}"
                )

            else:

                expanded.append(part)

        return expanded


intent_expander = IntentExpander()