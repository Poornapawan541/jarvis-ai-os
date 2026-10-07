"""
=========================================
JARVIS TASK MODEL
=========================================
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Task:
    """
    Represents one executable task.
    """

    action: str
    target: str = ""
    data: str = ""

    parameters: Dict = field(default_factory=dict)

    status: str = "pending"

    result: str = ""

    def complete(self, result=""):

        self.status = "completed"
        self.result = result

    def fail(self, reason=""):

        self.status = "failed"
        self.result = reason

    def __str__(self):

        return (
            f"Task("
            f"action='{self.action}', "
            f"target='{self.target}', "
            f"status='{self.status}')"
        )