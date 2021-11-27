from config.celery import app
from croncierge import cmd_services
from croncierge import models


@app.task(ignore_result=True, name="Run task")
def run_task(task_id):
    task = models.Task.objects.filter(id=task_id).first()
    if not task:
        return
    print(task.command)
    cmd_response = cmd_services.run_cmd(task.command)
    log = models.Log(
        task=task,
        stdout=cmd_response.stdout,
        stderr=cmd_response.stderr,
        status_code=cmd_response.status,
        started_at=cmd_response.started_at,
        exited_at=cmd_response.exited_at,
    )
    log.save()
