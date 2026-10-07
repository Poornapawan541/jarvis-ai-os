"""
=========================================
JARVIS EXECUTOR
=========================================
"""

from core.skills.router import router
from core.services.logger import logger


class Executor:

    def execute(self, tasks):

        logger.info(
            f"Starting execution of {len(tasks)} task(s)"
        )

        completed = []
        failed = []

        for index, task in enumerate(tasks, start=1):

            logger.info(
                f"[{index}/{len(tasks)}] "
                f"{task.action} {task.target}"
            )

            try:

                # -----------------------------
                # Chat task
                # -----------------------------
                if task.action == "chat":

                    logger.info(
                        "Chat task detected. "
                        "Skipping executor."
                    )

                    continue

                # -----------------------------
                # Build command
                # -----------------------------
                command = task.action

                if task.action == "search":
                    # For search tasks, target is the search engine.
                    # Only the actual query should be sent to the skill.
                    if task.data:
                        command += f" {task.data}"

                else:
                    if task.target:
                        command += f" {task.target}"

                    if task.data:
                        command += f" {task.data}"
                logger.info(
                    f"Executing command: {command}"
                )

                response = router.route(command)

                if response:

                    task.complete(response)

                    completed.append(task)

                    logger.info(
                        f"Task completed: {task.action}"
                    )

                else:

                    task.fail(
                        "No skill handled the task"
                    )

                    failed.append(task)

                    logger.warning(
                        f"No skill found for "
                        f"{task.action}"
                    )

            except Exception as e:

                task.fail(str(e))

                failed.append(task)

                logger.error(
                    f"Task failed: {e}"
                )

        logger.info(
            f"Execution finished. "
            f"Completed={len(completed)}, "
            f"Failed={len(failed)}"
        )

        return {
            "completed": completed,
            "failed": failed,
        }


executor = Executor()