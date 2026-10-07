"""
=========================================
JARVIS INTENT DETECTOR
=========================================
"""


class IntentDetector:

    OPEN = "open"
    CLOSE = "close"
    SEARCH = "search"
    CALCULATE = "calculate"
    CHAT = "chat"

    OPEN_WORDS = [
        "open",
        "launch",
        "start",
        "run",
    ]
    CLOSE_WORDS = [
        "close",
        "kill",
        "stop",
        "terminate",
    ]
    SEARCH_WORDS = [
        "search",
        "find",
        "look up",
        "google",
    ]

    def detect(self, text):

        text = text.lower().strip()

        # -----------------------------
        # OPEN
        # -----------------------------
        for word in self.OPEN_WORDS:

            if text.startswith(word):
                return self.OPEN
        # -----------------------------
        # CLOSE
        # -----------------------------
        for word in self.CLOSE_WORDS:

            if text.startswith(word):
                return self.CLOSE
        # -----------------------------
        # SEARCH
        # -----------------------------
        for word in self.SEARCH_WORDS:

            if text.startswith(word):
                return self.SEARCH

        # -----------------------------
        # CALCULATOR
        # -----------------------------
        if any(op in text for op in [
            "+",
            "-",
            "*",
            "/",
            "plus",
            "minus",
            "multiply",
            "multiplied by",
            "divided by",
            "divide",
        ]):
            return self.CALCULATE

        # -----------------------------
        # DEFAULT
        # -----------------------------
        return self.CHAT


intent_detector = IntentDetector()