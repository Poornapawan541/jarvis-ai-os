"""
=========================================
JARVIS BROWSER AGENT
=========================================
"""

from core.browser.actions import browser_actions
from core.services.logger import logger


class BrowserAgent:

    name = "browser"

    WEBSITES = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://github.com",
        "chatgpt": "https://chatgpt.com",
        "gmail": "https://mail.google.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "linkedin": "https://www.linkedin.com",
        "twitter": "https://twitter.com",
        "x": "https://x.com",
        "reddit": "https://www.reddit.com",
        "stackoverflow": "https://stackoverflow.com",
        "amazon": "https://www.amazon.com",
        "flipkart": "https://www.flipkart.com",
        "netflix": "https://www.netflix.com",
    }

    PREFIXES = (
        "open ",
        "visit ",
        "go to ",
        "browse ",
        "launch ",
    )

    def _extract_target(self, text):

        text = text.lower().strip()

        for prefix in self.PREFIXES:

            if text.startswith(prefix):

                return text[len(prefix):].strip()

        return None

    def can_handle(self, text):

        target = self._extract_target(text)

        if not target:
            return False

        # Remove common punctuation produced by Whisper
        target = target.rstrip(".,!?")

        return target in self.WEBSITES

    def execute(self, text):

        target = self._extract_target(text)

        if not target:
            return None

        target = target.rstrip(".,!?")

        url = self.WEBSITES.get(target)

        if not url:
            return None

        logger.info(
            f"Opening website: {target}"
        )

        try:

            result = browser_actions.open(url)

            if result:
                return result

            return f"Opening {target}."

        except Exception as e:

            logger.error(
                f"Failed to open {target}: {e}"
            )

            return (
                f"Sorry, I couldn't open {target}."
            )


browser_agent = BrowserAgent()