from core.planner.task import Task

task = Task(
    action="open",
    target="chrome"
)

print(task)

task.complete("Chrome opened successfully")

print(task.status)
print(task.result)