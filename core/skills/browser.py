"""
=========================================
JARVIS BROWSER SKILL
=========================================
"""

import os
import subprocess
from urllib.parse import quote_plus

from core.skills.base import Skill


class BrowserSkill(Skill):

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
        'whatsapp': 'https://web.whatsapp.com',
        "x": "https://x.com",
        "reddit": "https://www.reddit.com",
        "stackoverflow": "https://stackoverflow.com",
        "amazon": "https://www.amazon.in",
        "flipkart": "https://www.flipkart.com",
        "netflix": "https://www.netflix.com",
        "spotify": "https://open.spotify.com",
    }

    CHROME_PATHS = [
        os.path.expandvars(
            r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"
        ),
        os.path.expandvars(
            r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"
        ),
        os.path.expandvars(
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
        ),
    ]

    EDGE_PATHS = [
        os.path.expandvars(
            r"%PROGRAMFILES(X86)%\Microsoft\Edge\Application\msedge.exe"
        ),
        os.path.expandvars(
            r"%PROGRAMFILES%\Microsoft\Edge\Application\msedge.exe"
        ),
    ]

    def can_handle(self, text):

        text = text.lower().strip()

        # Search commands
        if text.startswith("search "):
            return True

        # Website opening
        if text.startswith("open "):

            target = text[5:].strip()

            return target in self.WEBSITES

        return False

    # =====================================
    # FIND CHROME
    # =====================================

    def _find_chrome(self):

        for path in self.CHROME_PATHS:

            if os.path.exists(path):
                return path

        return None

    # =====================================
    # FIND EDGE
    # =====================================

    def _find_edge(self):

        for path in self.EDGE_PATHS:

            if os.path.exists(path):
                return path

        return None

    # =====================================
    # OPEN URL IN CHROME
    # =====================================

    def _open_in_chrome(self, url):

        chrome = self._find_chrome()

        if chrome:

            subprocess.Popen(
                [
                    chrome,
                    url
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            return True

        return False

    # =====================================
    # OPEN URL IN EDGE
    # =====================================

    def _open_in_edge(self, url):

        edge = self._find_edge()

        if edge:

            subprocess.Popen(
                [
                    edge,
                    url
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            return True

        return False

    # =====================================
    # EXECUTE
    # =====================================

    def execute(self, text):

        text = text.lower().strip()

        # ---------------------------------
        # OPEN WEBSITE
        # ---------------------------------

        if text.startswith("open "):

            target = text[5:].strip()

            url = self.WEBSITES.get(target)

            if url:

                # Open website in desktop Chrome
                if self._open_in_chrome(url):

                    return f"Opening {target} in Chrome."

                # Fallback to Windows default browser
                try:

                    os.startfile(url)

                    return f"Opening {target}."

                except Exception:

                    return None

        # ---------------------------------
        # SEARCH GOOGLE
        # ---------------------------------

        if text.startswith("search "):

            query = text[7:].strip()

            if not query:

                return "What would you like me to search for?"

            url = (
                "https://www.google.com/search?q="
                + quote_plus(query)
            )

            # ---------------------------------
            # IMPORTANT:
            # Open Google Search in desktop Chrome
            # ---------------------------------

            if self._open_in_chrome(url):

                return f"Searching Google for {query}."

            # Fallback to Edge
            if self._open_in_edge(url):

                return f"Searching Google for {query}."

            # Final fallback
            try:

                os.startfile(url)

                return f"Searching Google for {query}."

            except Exception:

                return "Sorry, I couldn't open the browser."

        return None


browser = BrowserSkill()