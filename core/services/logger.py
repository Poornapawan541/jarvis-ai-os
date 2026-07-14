"""
=========================================
JARVIS LOGGER
=========================================
"""

import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "jarvis.log")

os.makedirs(LOG_DIR, exist_ok=True)


class Logger:

    def __init__(self):

        self.logger = logging.getLogger("Jarvis")

        if not self.logger.handlers:

            self.logger.setLevel(logging.INFO)

            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )

            # Console
            console = logging.StreamHandler()
            console.setFormatter(formatter)

            # File
            file = logging.FileHandler(LOG_FILE, encoding="utf-8")
            file.setFormatter(formatter)

            self.logger.addHandler(console)
            self.logger.addHandler(file)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)


logger = Logger()