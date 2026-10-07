"""
=========================================
JARVIS FOLLOW-UP RESOLVER
=========================================
"""

from core.conversation.history import history


class FollowUpResolver:

    FOLLOW_UPS = {
        "search videos": "videos",
        "search images": "images",
        "search news": "news",
        "search more": "",

        "show me videos": "videos",
        "show me images": "images",
        "show me more videos": "videos",
        "show me more images": "images",
        "show me more news": "news",

        "find more": "",
    }
    CLOSE_WORDS = {
        "close it",
        "close that",
        "close this",
        "close that application",
        "close this application",
        "close the application",
        "kill it",
        "stop it",
    }

    def get_last_search_query(self):
        messages = history.get_messages()

        for message in reversed(messages):

            if message["role"] != "user":
                continue

            text = message["content"].lower().strip()

            if text.startswith("search "):
                query = text[7:].strip()

                for suffix in [" videos", " images", " news"]:
                    if query.endswith(suffix):
                        query = query[:-len(suffix)].strip()

                return query

        return None

    def get_last_open_target(self):
        messages = history.get_messages()

        for message in reversed(messages):

            if message["role"] != "user":
                continue

            text = message["content"].lower().strip()

            for verb in ["open ", "launch ", "start ", "run "]:

                if text.startswith(verb):

                    target = text[len(verb):].strip()

                    for article in ["the ", "a ", "an ", "my "]:

                        if target.startswith(article):
                            target = target[len(article):].strip()
                            break

                    return target

        return None

    def resolve(self, text):

        text = text.strip()
        lower_text = text.lower().rstrip(".!?")

        # -----------------------------
        # Search follow-ups
        # -----------------------------
        if lower_text in self.FOLLOW_UPS:

            previous_query = self.get_last_search_query()

            if previous_query:

                suffix = self.FOLLOW_UPS[lower_text]

                if suffix:
                    return f"search {previous_query} {suffix}"

                return f"search {previous_query}"

        # -----------------------------
        # Open application follow-ups
        # -----------------------------
        if lower_text in {
            "open it",
            "open that",
            "open this",
            "open that application",
            "open this application",
        }:

            previous_target = self.get_last_open_target()

            if previous_target:
                return f"open {previous_target}"

        # -----------------------------
        # Application follow-ups
        # -----------------------------
        if lower_text in self.CLOSE_WORDS:

            previous_target = self.get_last_open_target()

            if previous_target:
                return f"close {previous_target}"

        return text


resolver = FollowUpResolver()