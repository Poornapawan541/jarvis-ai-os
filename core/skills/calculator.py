"""
=========================================
JARVIS CALCULATOR SKILL
=========================================
"""

from core.skills.base import Skill


class CalculatorSkill(Skill):

    name = "calculator"

    def can_handle(self, text):

        text = text.lower()

        keywords = [
            "calculate",
            "plus",
            "minus",
            "multiply",
            "divide",
            "+",
            "-",
            "*",
            "/",
        ]

        return any(word in text for word in keywords)

    def execute(self, text):

        expression = (
            text.lower()
            .replace("calculate", "")
            .replace("plus", "+")
            .replace("minus", "-")
            .replace("multiply", "*")
            .replace("divide", "/")
            .strip()
        )

        try:
            result = eval(expression, {"__builtins__": {}})
            return f"The answer is {result}."
        except Exception:
            return "Sorry, I couldn't calculate that."


calculator = CalculatorSkill()