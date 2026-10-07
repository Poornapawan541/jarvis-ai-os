"""
=========================================
JARVIS BROWSER MANAGER
=========================================
"""

import os
import subprocess


class BrowserManager:

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
            r"%PROGRAMFILES%\Microsoft\Edge\Application\msedge.exe"
        ),
        os.path.expandvars(
            r"%PROGRAMFILES(X86)%\Microsoft\Edge\Application\msedge.exe"
        ),
    ]

    def __init__(self):
        self.browser = "chrome"

    # =====================================
    # FIND CHROME
    # =====================================

    def find_chrome(self):

        for path in self.CHROME_PATHS:

            if os.path.exists(path):
                return path

        return None

    # =====================================
    # FIND EDGE
    # =====================================

    def find_edge(self):

        for path in self.EDGE_PATHS:

            if os.path.exists(path):
                return path

        return None

    # =====================================
    # OPEN IN CHROME
    # =====================================

    def open_chrome(self, url):

        chrome = self.find_chrome()

        if not chrome:
            return "Chrome was not found on this computer."

        try:

            subprocess.Popen(
                [
                    chrome,
                    url
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            return f"Opened {url} in Chrome."

        except Exception as e:

            return f"Failed to open Chrome: {e}"

    # =====================================
    # OPEN IN EDGE
    # =====================================

    def open_edge(self, url):

        edge = self.find_edge()

        if not edge:
            return "Microsoft Edge was not found on this computer."

        try:

            subprocess.Popen(
                [
                    edge,
                    url
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            return f"Opened {url} in Edge."

        except Exception as e:

            return f"Failed to open Edge: {e}"

    # =====================================
    # OPEN URL
    # =====================================

    def open(self, url):

        if self.browser == "edge":
            return self.open_edge(url)

        return self.open_chrome(url)

    # =====================================
    # CHANGE BROWSER
    # =====================================

    def use_chrome(self):

        self.browser = "chrome"
        return "Chrome selected."

    def use_edge(self):

        self.browser = "edge"
        return "Edge selected."

    # =====================================
    # CLOSE
    # =====================================

    def close(self):

        # IMPORTANT:
        # Do NOT close Chrome or Edge here.
        #
        # Jarvis should not close the user's
        # personal browser when Jarvis exits.

        return


browser_manager = BrowserManager()