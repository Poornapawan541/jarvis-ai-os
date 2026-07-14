"""
=========================================
JARVIS BASE SKILL
=========================================
"""


class Skill:

    name = "base"

    def can_handle(self, text):
        return False

    def execute(self, text):
        return None