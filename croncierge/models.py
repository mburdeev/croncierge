from django.db import models

class Task(models.Model):
    command = models.CharField(max_length=1024)
    # TODO расписание

    def __str__(self):
        return f"<Task (id{self.id}): {self.command[:15]}>"

class Log(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    stdout = models.TextField()
    stderr = models.TextField()
    status_code = models.IntegerField()
    started_at = models.DateTimeField()
    exited_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"<Log (task:{self.id})>"
