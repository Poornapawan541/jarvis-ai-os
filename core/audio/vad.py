"""
=========================================
Voice Activity Detection (VAD)
=========================================
"""

import numpy as np


class VoiceActivityDetector:
    def __init__(
        self,
        threshold=0.02,
        silence_duration=1.0,
        sample_rate=16000,
        chunk_size=1024,
    ):
        self.threshold = threshold
        self.silence_duration = silence_duration
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size

        self.required_silent_chunks = int(
            (sample_rate * silence_duration) / chunk_size
        )

        self.silent_chunks = 0

    def is_speaking(self, audio_chunk):

        level = np.max(np.abs(audio_chunk))

        return level > self.threshold

    def should_stop(self, audio_chunk):

        if self.is_speaking(audio_chunk):
            self.silent_chunks = 0
            return False

        self.silent_chunks += 1

        return self.silent_chunks >= self.required_silent_chunks