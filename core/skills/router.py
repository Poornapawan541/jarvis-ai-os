"""
=========================================
JARVIS SKILL ROUTER
=========================================
"""

from core.skills.calculator import calculator


class SkillRouter:

    def __init__(self):
        self.skills = [
            calculator,
        ]

    def route(self, text):

        for skill in self.skills:

            if skill.can_handle(text):
                return skill.execute(text)

        return None


router = SkillRouter()