"""
=========================================
JARVIS SKILL BASE CLASS
=========================================
"""


class Skill:

    name = "base"

    def can_handle(self, text):
        """
        Return True if this skill can
        handle the given command.
        """
        raise NotImplementedError

    def execute(self, text):
        """
        Execute the command and
        return a response string.
        """
        raise NotImplementedError