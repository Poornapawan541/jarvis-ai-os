"""
=========================================
JARVIS BROWSER ACTIONS
=========================================
"""

from core.browser.manager import browser_manager


class BrowserActions:

    def open(self, url):

        return browser_manager.open(url)

    def search_google(self, query):

        url = (
            "https://www.google.com/search?q="
            + query.replace(" ", "+")
        )

        return browser_manager.open(url)

    def search_youtube(self, query):

        url = (
            "https://www.youtube.com/results?search_query="
            + query.replace(" ", "+")
        )

        return browser_manager.open(url)

    def goto(self, url):

        browser_manager.session.start()

        browser_manager.session.page.goto(url)

        return "Navigation complete."

    def click(self, selector):

        browser_manager.session.page.click(selector)

        return "Clicked."

    def type(self, selector, text):

        browser_manager.session.page.fill(
            selector,
            text,
        )

        return "Typed."

    def press(self, key):

        browser_manager.session.page.keyboard.press(
            key
        )

        return "Key pressed."

    def wait(self, seconds):

        browser_manager.session.page.wait_for_timeout(
            seconds * 1000
        )

        return "Wait completed."

    def title(self):

        return browser_manager.session.page.title()

    def url(self):

        return browser_manager.session.page.url


browser_actions = BrowserActions()