from core.parser.command_parser import parser

tests = [
    "Please open Chrome",
    "Could you launch VS Code?",
    "Can you start calculator?",
    "Run notepad",
]

for text in tests:

    print(text)
    print(" -> ", parser.normalize(text))