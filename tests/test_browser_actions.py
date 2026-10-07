from core.browser.actions import browser_actions

browser_actions.search_google(
    "Artificial Intelligence"
)

browser_actions.wait(3)

print(browser_actions.title())

input("Press Enter...")