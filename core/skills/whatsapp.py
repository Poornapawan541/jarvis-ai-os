from playwright.sync_api import sync_playwright
from core.skills.base import Skill
import re

class WhatsAppSkill(Skill):
    name = "whatsapp"

    WHATSAPP_URL = "https://web.whatsapp.com"
    CDP_URL = "http://127.0.0.1:9222"

    def can_handle(self, text):
        text = text.lower().strip()
        return text.startswith("send a whatsapp message")

    def execute(self, text):
        text = text.strip()

        prefix = "send a whatsapp message to "

        if not text.lower().startswith(prefix):
            return "Please specify a WhatsApp contact and message."

        content = text[len(prefix):].strip()

        marker = " saying "

        if marker not in content.lower():
            return "Please specify what you want me to say."

        index = content.lower().index(marker)

        contact = content[:index].strip()
        message = content[index + len(marker):].strip()

        if not contact:
            return "Please specify the WhatsApp contact."

        if not message:
            return "Please specify the message."

        return self.send_message(contact, message)

    def send_message(self, contact, message):
        p = sync_playwright().start()

        try:
            # Connect to the already-running Chrome
            browser = p.chromium.connect_over_cdp(
                self.CDP_URL
            )

            if not browser.contexts:
                return "Chrome browser context was not found."

            context = browser.contexts[0]

            # Use an existing tab if available
            page = context.pages[0] if context.pages else context.new_page()

            page.goto(self.WHATSAPP_URL)
            page.wait_for_timeout(5000)

            # Find the contact
            chat = page.locator(
                '[data-testid="cell-frame-title"] span'
            ).filter(
                has_text=re.compile(re.escape(contact), re.IGNORECASE)
            )

            if chat.count() == 0:
                return f"Could not find WhatsApp contact {contact}."

            chat.first.click()
            page.wait_for_timeout(2000)

            # Find message box
            message_box = page.locator(
                '[data-testid="conversation-compose-box-input"]'
            )

            if message_box.count() == 0:
                return "Could not find the WhatsApp message box."

            # Send message
            message_box.fill(message)
            page.keyboard.press("Enter")

            page.wait_for_timeout(2000)

            return f"WhatsApp message sent to {contact}."

        except Exception as e:
            return f"Sorry, I couldn't send the WhatsApp message: {e}"

        finally:
            # IMPORTANT:
            # Do NOT close browser/context.
            # They belong to the user's existing Chrome session.
            p.stop()


whatsapp = WhatsAppSkill()