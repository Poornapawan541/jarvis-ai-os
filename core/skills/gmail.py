import os
import base64
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from core.skills.base import Skill
from core.brain.llm import llm

from html import unescape
import re



class GmailSkill(Skill):
    name = "gmail"

    def normalize_email_address(self, text):
        email = text.lower().strip()

        replacements = {
            " at the rate ": "@",
            " at rate ": "@",
            " at ": "@",
            " dot ": ".",
            " period ": ".",
            " ": "",
        }

        for old, new in replacements.items():
            email = email.replace(old, new)

        email = email.rstrip(".,!?")

        return email

    def set_voice_functions(self, listen, speak):
            self.listen = listen
            self.speak = speak

    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
              "https://www.googleapis.com/auth/gmail.send"]
    def is_valid_email(self, email):
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        return re.match(pattern, email) is not None
    def send_email_conversation(self, to):
        if not hasattr(self, "listen") or not hasattr(self, "speak"):
            return "Voice input is not available."

        if not self.is_valid_email(to):
            return "I couldn't understand a valid email address. Please say the email address again."

        self.speak("What is the subject?")
        subject = self.listen()

        if not subject:
            return "I didn't hear the subject."

        self.speak("What should I say?")
        body = self.listen()

        if not body:
            return "I didn't hear the message."

        self.speak("Sending the email.")

        return self.send_email(to, subject, body)

    def send_email_conversation(self, to):
        if not hasattr(self, "listen") or not hasattr(self, "speak"):
            return "Voice input is not available."

        self.speak("What is the subject?")
        subject = self.listen()

        if not subject:
            return "I didn't hear the subject."

        self.speak("What should I say?")
        body = self.listen()

        if not body:
            return "I didn't hear the message."

        self.speak("Sending the email.")

        return self.send_email(to, subject, body)

    def can_handle(self, text):
        text = text.lower().strip()

        keywords = [
            "read my emails",
            "read my email",
            "read emails",
            "read email",
            "check my emails",
            "check my email",
            "check emails",
            "check email",
            "today's emails",
            "todays emails",
            "emails today",

            "send an email",
            "send email",
            "send a mail",
            "send mail",
            "email",
            "mail",
        ]

        return any(keyword in text for keyword in keywords)

    def get_email_body(self, payload):
        plain_text = ""
        html_text = ""

        if "parts" in payload:
            for part in payload["parts"]:
                mime_type = part.get("mimeType", "")

                if mime_type == "text/plain":
                    data = part.get("body", {}).get("data")

                    if data:
                        plain_text += base64.urlsafe_b64decode(
                            data
                        ).decode("utf-8", errors="ignore")

                elif mime_type == "text/html":
                    data = part.get("body", {}).get("data")

                    if data:
                        html_text += base64.urlsafe_b64decode(
                            data
                        ).decode("utf-8", errors="ignore")

                elif "parts" in part:
                    nested_text = self.get_email_body(part)

                    if nested_text:
                        plain_text += nested_text

        else:
            data = payload.get("body", {}).get("data")

            if data:
                decoded = base64.urlsafe_b64decode(
                    data
                ).decode("utf-8", errors="ignore")

                if payload.get("mimeType") == "text/html":
                    html_text += decoded
                else:
                    plain_text += decoded

        # Prefer normal plain text when available.
        if plain_text.strip():
            return plain_text.strip()

        # Convert HTML to readable text.
        if html_text.strip():
            text = unescape(html_text)

            text = re.sub(
                r"<(script|style).*?>.*?</\1>",
                " ",
                text,
                flags=re.IGNORECASE | re.DOTALL
            )

            text = re.sub(
                r"<br\s*/?>",
                "\n",
                text,
                flags=re.IGNORECASE
            )

            text = re.sub(
                r"</p\s*>",
                "\n",
                text,
                flags=re.IGNORECASE
            )

            text = re.sub(
                r"<[^>]+>",
                " ",
                text
            )

            text = re.sub(
                r"[ \t]+",
                " ",
                text
            )

            text = re.sub(
                r"\n\s*\n+",
                "\n",
                text
            )

            return text.strip()

        return ""
    def summarize_email(self, sender, subject, body):
        if not body:
            return f"Email from {sender} with subject {subject}. The email has no readable text."

        # Prevent extremely large emails from consuming the context.
        body = body[:8000]

        prompt = f"""
You are Jarvis, a personal AI assistant.

Summarize this email for the user in simple spoken English.

Sender:
{sender}

Subject:
{subject}

Email:
{body}

Give:
1. What the email is about
2. Important information
3. Any action the user needs to take
4. Important date/time if mentioned

Keep it concise, around 2-4 sentences.
Do not invent information.
"""

        try:
            return llm.ask(prompt).strip()
        except Exception:
            return f"Email from {sender} about {subject}."

    def execute(self, text):
        text_lower = text.lower().strip()

        if text_lower.startswith("send an email to "):
            recipient = text[len("send an email to "):].strip()
            recipient = self.normalize_email_address(recipient)

            return self.send_email_conversation(recipient)

        if not os.path.exists("token.json"):
            return "Gmail is not connected yet."

        try:
            creds = Credentials.from_authorized_user_file(
                "token.json",
                self.SCOPES
            )

            service = build(
                "gmail",
                "v1",
                credentials=creds
            )

            today = datetime.now().date()
            tomorrow = today + timedelta(days=1)

            today_str = today.strftime("%Y/%m/%d")
            tomorrow_str = tomorrow.strftime("%Y/%m/%d")

            query = (
                f"after:{today_str} "
                f"before:{tomorrow_str} "
                "-in:sent "
                "-in:drafts "
                "-in:spam "
                "-in:trash"
            )

            messages = []
            page_token = None

            while True:
                response = service.users().messages().list(
                    userId="me",
                    q=query,
                    maxResults=100,
                    pageToken=page_token
                ).execute()

                messages.extend(
                    response.get("messages", [])
                )

                page_token = response.get("nextPageToken")

                if not page_token:
                    break

            if not messages:
                return "You didn't receive any emails today."

            email_data = []

            for message in messages:
                email = service.users().messages().get(
                    userId="me",
                    id=message["id"],
                    format="full"
                ).execute()

                payload = email.get("payload", {})
                headers = payload.get("headers", [])

                data = {}

                for header in headers:
                    data[header["name"]] = header["value"]

                sender = data.get("From", "Unknown sender")
                subject = data.get("Subject", "No subject")
                date = data.get("Date", "Unknown date")

                body = self.get_email_body(payload)

                labels = email.get("labelIds", [])

                if "CATEGORY_PROMOTIONS" in labels:
                    category = "Promotions"
                elif "CATEGORY_SOCIAL" in labels:
                    category = "Social"
                elif "CATEGORY_UPDATES" in labels:
                    category = "Updates"
                elif "CATEGORY_FORUMS" in labels:
                    category = "Forums"
                else:
                    category = "Main"

                email_data.append(
                    f"""
    EMAIL {len(email_data) + 1}

    Category: {category}

    From:
    {sender}

    Subject:
    {subject}

    Date:
    {date}

    Content:
    {body[:8000]}
    """
                )

            all_emails = "\n".join(email_data)

            prompt = f"""
    You are Jarvis, a personal AI assistant.

    The user asked:

    "Read my emails."

    These are ALL emails received today:

    {all_emails}

    Your job is to summarize today's emails for the user.

    IMPORTANT RULES:

    1. INCLUDE EVERY EMAIL.
    2. NEVER omit an email.
    3. Do not invent information.
    4. Do not repeat the same email in multiple sections.
    5. Do not say "Hello, I'm Jarvis" or similar introductions.
    6. Use simple natural spoken English.
    7. Do not include email addresses unless they are useful.
    8. Do not read long URLs aloud.
    9. Keep the response reasonably concise.

    Use EXACTLY this structure:

    TODAY'S EMAILS

    Start with:
    "You received X emails today."

    Then list EVERY email.

    For each email give:
    - Sender
    - Subject
    - A short 1-2 sentence summary

    IMPORTANT EMAILS

    Identify only emails that genuinely require attention.

    For each important email:
    - Explain what it is about
    - Explain why it matters
    - State what action is needed
    - Mention deadline/date/time if present

    Do NOT repeat the entire email.
    Do NOT repeat the normal summary.

    PROMOTIONS

    If there are promotional emails:
    Give each one 1-2 short bullet points.

    If there are none:
    Say:
    "No new promotional emails today."

    SOCIAL

    If there are social emails:
    Give each one 1-2 short bullet points.

    If there are none:
    Say:
    "No new social emails today."

    UPDATES

    If there are update emails:
    Give each one 1-2 short bullet points.

    If there are none:
    Say:
    "No new update emails today."

    IMPORTANT CATEGORY RULE:

    Use the Gmail category supplied with each email.

    Do not guess categories.

    IMPORTANT EMAIL RULE:

    An email can be important even if it belongs to Updates,
    Promotions, Social, or another category.

    However, if an email is already described in IMPORTANT EMAILS,
    do not repeat its full details in another section.

    Keep the final answer suitable for text-to-speech.
    """

            # ONE Ollama call for the complete day's emails.
            result = llm.ask(prompt)

            if not result:
                return "I couldn't summarize today's emails."

            return result.strip()

        except Exception as e:
            return f"Sorry, I couldn't read today's emails: {e}"
gmail_skill = GmailSkill()
