"""
=========================================
JARVIS PLANNER
=========================================
"""

from core.planner.task import Task
from core.planner.intent import intent_detector
from core.planner.parser import parser
from core.planner.intent_expander import intent_expander

class Planner:

    def create_plan(self, user_input):

        tasks = []

        # Normalize and split the sentence into commands
        commands = parser.parse(user_input)

        expanded_commands = []

        for command in commands:
            expanded_commands.extend(
                intent_expander.expand(command)
            )

        commands = expanded_commands

        for command in commands:

            intent = intent_detector.detect(command)

            # ----------------------------------
            # OPEN
            # ----------------------------------
            if intent == intent_detector.OPEN:

                target = command

                for word in intent_detector.OPEN_WORDS:
                    if target.startswith(word):
                        target = target[len(word):].strip()
                        break

                # Remove common articles/pronouns
                for word in ["the ", "a ", "an ", "my "]:
                    if target.startswith(word):
                        target = target[len(word):].strip()
                        break

                tasks.append(
                    Task(
                        action="open",
                        target=target,
                    )
                )

                continue
            # ----------------------------------
            # CLOSE
            # ----------------------------------
            if intent == intent_detector.CLOSE:

                target = command

                for word in intent_detector.CLOSE_WORDS:
                    if target.startswith(word):
                        target = target[len(word):].strip()
                        break

                # Remove common articles/pronouns
                for word in ["the ", "a ", "an ", "my "]:
                    if target.startswith(word):
                        target = target[len(word):].strip()
                        break

                tasks.append(
                    Task(
                        action="close",
                        target=target,
                    )
                )

                continue
            # ----------------------------------
            # SEARCH
            # ----------------------------------
            if intent == intent_detector.SEARCH:

                query = command

                for word in intent_detector.SEARCH_WORDS:
                    if query.startswith(word):
                        query = query[len(word):].strip()
                        break

                tasks.append(
                    Task(
                        action="search",
                        target="google",
                        data=query,
                    )
                )

                continue

            # ----------------------------------
            # CALCULATE
            # ----------------------------------
            if intent == intent_detector.CALCULATE:

                tasks.append(
                    Task(
                        action="calculate",
                        data=command,
                    )
                )

                continue

            # ----------------------------------
            # CHAT
            # ----------------------------------
            tasks.append(
                Task(
                    action="chat",
                    data=command,
                )
            )

        return tasks


planner = Planner()