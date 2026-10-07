"""
=========================================
JARVIS WAKE WORD DETECTOR
=========================================
"""

import numpy as np

from core.audio.recorder import record_audio


class WakeWordDetector:

    def __init__(self):

        self.wake_words = {
            "jarvis",
            "jarosh",
            "jarves",
        }

    def detect(self, text):

        if not text:
            return False

        text = text.lower().strip()

        # Remove punctuation
        text = "".join(
            char
            for char in text
            if char.isalnum() or char.isspace()
        )

        words = text.split()

        return any(
            word in self.wake_words
            for word in words
        )


wake_word_detector = WakeWordDetector()