"""
=========================================
JARVIS AI - Windows System Skill
=========================================
Handles direct Windows system/application commands.
"""

import subprocess
import webbrowser

from core.skills.base import Skill
from core.services.logger import logger


class SystemSkill(Skill):

    name = "system"

    description = (
        "Controls Windows applications and system functions. "
        "Can open and close applications, open folders, "
        "lock the computer, shutdown, restart, etc."
    )

    def __init__(self):

        self.apps = {
            "notepad": "notepad.exe",

            "calculator": "calc.exe",
            "calc": "calc.exe",

            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",

            "edge": "msedge.exe",
            "microsoft edge": "msedge.exe",

            "explorer": "explorer.exe",
            "file explorer": "explorer.exe",

            "paint": "mspaint.exe",

            "word": "winword.exe",
            "microsoft word": "winword.exe",

            "excel": "excel.exe",
            "microsoft excel": "excel.exe",

            "powerpoint": "powerpnt.exe",
            "microsoft powerpoint": "powerpnt.exe",
        }

        self.process_map = {
            "notepad": "notepad.exe",

            "calculator": "CalculatorApp.exe",
            "calc": "CalculatorApp.exe",

            "chrome": "chrome.exe",
            "google chrome": "chrome.exe",

            "edge": "msedge.exe",
            "microsoft edge": "msedge.exe",

            "explorer": "explorer.exe",
            "file explorer": "explorer.exe",

            "paint": "mspaint.exe",

            "word": "WINWORD.EXE",
            "microsoft word": "WINWORD.EXE",

            "excel": "EXCEL.EXE",
            "microsoft excel": "EXCEL.EXE",

            "powerpoint": "POWERPNT.EXE",
            "microsoft powerpoint": "POWERPNT.EXE",
        }

        self.sites = {
            "github": "https://github.com",
            "gmail": "https://mail.google.com",
            "google": "https://google.com",
            "youtube": "https://youtube.com",
            "linkedin": "https://linkedin.com",
            "instagram": "https://instagram.com",
            "facebook": "https://facebook.com",
            "chatgpt": "https://chatgpt.com"
        }

    OPEN_VERBS = (
        "open ",
        "launch ",
        "start ",
        "run ",
    )

    CLOSE_VERBS = (
        "close ",
        "kill ",
        "stop ",
        "terminate ",
    )

    ARTICLES = (
        "the ",
        "a ",
        "an ",
        "my ",
    )

    def _extract_target(self, text: str, verbs) -> str:
        text = text.lower().strip().rstrip(".,!?")
        for verb in verbs:
            if text.startswith(verb):
                target = text[len(verb):].strip()
                for article in self.ARTICLES:
                    if target.startswith(article):
                        target = target[len(article):].strip()
                return target
        return ""

    def _is_lock_command(self, text: str) -> bool:
        text = text.lower().strip().rstrip(".,!?")
        return text in {
            "lock",
            "lock computer",
            "lock the computer",
            "lock workstation",
            "lock screen",
        }

    def _is_shutdown_command(self, text: str) -> bool:
        text = text.lower().strip().rstrip(".,!?")
        return text in {
            "shutdown",
            "shut down",
            "shutdown computer",
            "shut down computer",
            "shut down the computer",
            "turn off computer",
        }

    def _is_restart_command(self, text: str) -> bool:
        text = text.lower().strip().rstrip(".,!?")
        return text in {
            "restart",
            "reboot",
            "restart computer",
            "restart the computer",
            "reboot computer",
        }

    # =====================================
    # CAN HANDLE
    # =====================================

    def can_handle(self, text: str):

        text = text.lower().strip().rstrip(".,!?")

        open_target = self._extract_target(text, self.OPEN_VERBS)
        if open_target and (open_target in self.apps or open_target in self.sites):
            return True

        close_target = self._extract_target(text, self.CLOSE_VERBS)
        if close_target and (close_target in self.process_map or close_target in self.apps):
            return True

        if (
            self._is_lock_command(text)
            or self._is_shutdown_command(text)
            or self._is_restart_command(text)
        ):
            return True

        return False

    # =====================================
    # EXECUTE
    # =====================================

    def execute(self, text: str):

        text = text.lower().strip().rstrip(".,!?")

        logger.info(
            f"System skill handling: {text}"
        )

        # ---------------------------------
        # OPEN
        # ---------------------------------
        open_target = self._extract_target(text, self.OPEN_VERBS)
        if open_target:
            if open_target in self.sites:
                return self.open_website(open_target)
            if open_target in self.apps:
                return self.open_application(open_target)

        # ---------------------------------
        # CLOSE
        # ---------------------------------
        close_target = self._extract_target(text, self.CLOSE_VERBS)
        if close_target:
            return self.close_application(close_target)

        # ---------------------------------
        # LOCK
        # ---------------------------------
        if self._is_lock_command(text):
            return self.lock()

        # ---------------------------------
        # SHUTDOWN
        # ---------------------------------
        if self._is_shutdown_command(text):
            return self.shutdown()

        # ---------------------------------
        # RESTART
        # ---------------------------------
        if self._is_restart_command(text):
            return self.restart()

        return None

    # =====================================
    # OPEN APPLICATION
    # =====================================

    def open_application(self, app_name: str):

        app_name = app_name.lower().strip()

        executable = self.apps.get(app_name)

        if not executable:
            return f"I don't know how to open {app_name} yet."

        try:

            subprocess.Popen(
                executable,
                shell=False,
            )

            logger.info(
                f"Opened application: {app_name}"
            )

            return f"Opening {app_name}."

        except Exception as e:

            logger.error(
                f"Failed to open {app_name}: {e}"
            )

            return f"I couldn't open {app_name}."

    # =====================================
    # CLOSE APPLICATION
    # =====================================

    def close_application(self, app_name: str):

        app_name = app_name.lower().strip()

        process = self.process_map.get(app_name)

        if not process:
            return f"I don't know how to close {app_name} yet."

        try:

            result = subprocess.run(
                [
                    "taskkill",
                    "/F",
                    "/IM",
                    process
                ],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                logger.info(f"Closed application: {app_name}")
                return f"Closed {app_name}."

            logger.error(
                f"Failed to close {app_name}: "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )
            return f"I couldn't close {app_name}."
        except Exception as e:

            logger.error(
                f"Failed to close {app_name}: {e}"
            )

            return f"I couldn't close {app_name}."

    # =====================================
    # OPEN WEBSITE
    # =====================================

    def open_website(self, site: str):

        site = site.lower().strip()

        url = self.sites.get(site)

        if not url:

            if (
                site.startswith("http://")
                or site.startswith("https://")
            ):
                url = site

            else:
                url = f"https://www.{site}.com"

        try:

            webbrowser.open(url)

            logger.info(
                f"Opened website: {url}"
            )

            return f"Opening {site}."

        except Exception as e:

            logger.error(
                f"Failed to open {site}: {e}"
            )

            return f"I couldn't open {site}."

    # =====================================
    # LOCK COMPUTER
    # =====================================

    def lock(self):

        try:

            subprocess.run(
                [
                    "rundll32.exe",
                    "user32.dll,LockWorkStation"
                ]
            )

            return "Locking your computer."

        except Exception as e:

            logger.error(
                f"Lock failed: {e}"
            )

            return "I couldn't lock the computer."

    # =====================================
    # SHUTDOWN
    # =====================================

    def shutdown(self):

        try:

            subprocess.Popen(
                [
                    "shutdown",
                    "/s",
                    "/t",
                    "5"
                ]
            )

            return "The computer will shut down in 5 seconds."

        except Exception as e:

            logger.error(
                f"Shutdown failed: {e}"
            )

            return "I couldn't shut down the computer."

    # =====================================
    # RESTART
    # =====================================

    def restart(self):

        try:

            subprocess.Popen(
                [
                    "shutdown",
                    "/r",
                    "/t",
                    "5"
                ]
            )

            return "The computer will restart in 5 seconds."

        except Exception as e:

            logger.error(
                f"Restart failed: {e}"
            )

            return "I couldn't restart the computer."

    def handle(self, text: str):
        """Backward-compatible alias for execute."""
        return self.execute(text)


# =========================================
# GLOBAL INSTANCE
# =========================================

system_skill = SystemSkill()
