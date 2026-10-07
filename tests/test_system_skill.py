from core.skills.system import system_skill


print("=" * 50)
print("JARVIS SYSTEM SKILL TEST")
print("=" * 50)


commands = [
    "open calculator",
    "open the calculator",
    "launch calculator",
    "launch the calculator",
    "start calculator",
    "open notepad",
    "open the notepad",
]


for command in commands:

    result = system_skill.can_handle(command)

    print(
        f"{'✅' if result else '❌'} "
        f"{command:<30} -> {result}"
    )