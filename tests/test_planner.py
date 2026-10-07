from core.planner.planner import planner

tests = [

    "Open Chrome",

    "Search Python tutorials",

    "Open Chrome and Search AI News",

    "10 + 25",

    "Who is Elon Musk?",

]

for text in tests:

    print("=" * 50)

    print(text)

    tasks = planner.create_plan(text)

    for task in tasks:

        print(task)