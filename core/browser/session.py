"""
=========================================
JARVIS BROWSER SESSION
=========================================
"""

from playwright.sync_api import sync_playwright


class BrowserSession:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):

        # Already running
        if (
            self.browser
            and self.browser.is_connected()
            and self.page
            and not self.page.is_closed()
        ):
            return

        # Clean up stale session
        self.close()

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.context = self.browser.new_context()

        self.page = self.context.new_page()

    def close(self):

        try:
            if self.page and not self.page.is_closed():
                self.page.close()
        except Exception:
            pass

        try:
            if self.context:
                self.context.close()
        except Exception:
            pass

        try:
            if self.browser:
                self.browser.close()
        except Exception:
            pass

        try:
            if self.playwright:
                self.playwright.stop()
        except Exception:
            pass

        self.page = None
        self.context = None
        self.browser = None
        self.playwright = None