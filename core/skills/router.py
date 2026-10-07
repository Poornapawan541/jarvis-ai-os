"""
=========================================
JARVIS SKILL ROUTER
=========================================
"""

import importlib
import pkgutil

import core.skills

from core.services.logger import logger
from core.skills.base import Skill


class SkillRouter:

    def __init__(self):

        self.skills = []

        self.load_skills()

    # -------------------------------------
    # LOAD SKILLS
    # -------------------------------------

    def load_skills(self):

        logger.info("Loading skills...")

        package = core.skills

        self.skills.clear()

        for _, module_name, _ in pkgutil.iter_modules(
            package.__path__
        ):

            if module_name in ("router", "base"):
                continue

            try:

                module = importlib.import_module(
                    f"core.skills.{module_name}"
                )

                for attribute_name in dir(module):

                    obj = getattr(
                        module,
                        attribute_name
                    )

                    if isinstance(obj, type):
                        continue

                    if not isinstance(obj, Skill):
                        continue

                    if obj in self.skills:
                        continue

                    self.skills.append(obj)

                    logger.info(
                        f"Loaded skill: {obj.name}"
                    )

            except Exception as e:

                logger.error(
                    f"Failed to load skill "
                    f"'{module_name}': {e}"
                )

        logger.info(
            f"{len(self.skills)} skills loaded."
        )

    # -------------------------------------
    # ROUTE REQUEST
    # -------------------------------------

    def route(self, text):

        text = text.lower().strip()

        for skill in self.skills:

            try:

                if not skill.can_handle(text):
                    continue

                logger.info(
                    f"Skill selected: {skill.name}"
                )

                result = skill.execute(text)

                if result is not None:
                    return result

                logger.warning(
                    f"Skill '{skill.name}' "
                    f"could not execute request."
                )

            except Exception as e:

                logger.error(
                    f"Skill '{skill.name}' failed: {e}"
                )

        return None


router = SkillRouter()