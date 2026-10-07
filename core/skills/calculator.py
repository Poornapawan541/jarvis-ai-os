"""
=========================================
JARVIS CALCULATOR SKILL
=========================================
"""

from core.skills.base import Skill


class CalculatorSkill(Skill):

    name = "calculator"

    def can_handle(self, text):
        text = text.lower().strip()

        # Calculator skill should only handle a standalone calculation.
        if " and " in text:
            return False

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

        expression = text.lower().strip()

        # Remove polite command prefixes
        prefixes = [
            "please ",
            "can you ",
            "could you ",
            "would you ",
            "will you ",
        ]

        for prefix in prefixes:
            if expression.startswith(prefix):
                expression = expression[len(prefix):].strip()
                break

        # Remove calculation phrases
        expression = expression.replace("what is", "")
        expression = expression.replace("calculate", "")

        # Normalize word operators
        expression = expression.replace("divided by", "/")
        expression = expression.replace("multiply", "*")
        expression=expression.replace("multiplied by","*")
        expression = expression.replace("plus", "+")
        expression = expression.replace("minus", "-")
        expression = expression.replace("divide", "/")

        expression = expression.strip()

        try:
            result = eval(expression, {"__builtins__": {}})
            return f"The answer is {result}."
        except Exception:
            return "Sorry, I couldn't calculate that."

calculator = CalculatorSkill()