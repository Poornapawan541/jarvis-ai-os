from core.planner.planner import planner
from core.planner.executor import executor

tasks = planner.create_plan("Open notepad")

results = executor.execute(tasks)

for task in results:

    print(task)
    print(task.status)
    print(task.result)