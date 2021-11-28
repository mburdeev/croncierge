import uuid
import logging
from datetime import datetime

from django.db import models
from django_celery_beat.models import (
    CrontabSchedule, PeriodicTask, IntervalSchedule,
    SolarSchedule, ClockedSchedule
)
from django.utils.translation import gettext_lazy as _
from django.db.models import signals


logger = logging.getLogger(__name__)


class Task(models.Model):
    command = models.CharField(max_length=1024)
    
    # You can only set ONE of the following schedule FK's
    # TODO: Redo this as a GenericForeignKey
    interval = models.ForeignKey(
        IntervalSchedule, on_delete=models.CASCADE,
        null=True, blank=True, verbose_name=_('Interval Schedule'),
        help_text=_('Interval Schedule to run the task on.  '
                    'Set only one schedule type, leave the others null.'),
    )
    crontab = models.ForeignKey(
        CrontabSchedule, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_('Crontab Schedule'),
        help_text=_('Crontab Schedule to run the task on.  '
                    'Set only one schedule type, leave the others null.'),
    )
    solar = models.ForeignKey(
        SolarSchedule, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_('Solar Schedule'),
        help_text=_('Solar Schedule to run the task on.  '
                    'Set only one schedule type, leave the others null.'),
    )
    clocked = models.ForeignKey(
        ClockedSchedule, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_('Clocked Schedule'),
        help_text=_('Clocked Schedule to run the task on.  '
                    'Set only one schedule type, leave the others null.'),
    )

    one_off = models.BooleanField(
        default=False,
        verbose_name=_('One-off Task'),
        help_text=_(
            'If True, the schedule will only run the task a single time'),
    )
    start_time = models.DateTimeField(
        blank=True, null=True,
        verbose_name=_('Start Datetime'),
        help_text=_(
            'Datetime when the schedule should begin '
            'triggering the task to run'),
    )
    enabled = models.BooleanField(
        default=True,
        verbose_name=_('Enabled'),
        help_text=_('Set to False to disable the schedule'),
    )

    # Задача celery-beat
    periodic_task = models.ForeignKey(
        PeriodicTask, on_delete=models.CASCADE, null=True, blank=True,
        related_name='_periodic_task'
    )

    def validate_periodic_task(self, *args, **kwargs):
        debug_periodic_task = PeriodicTask(
                name=uuid.uuid4(),
                task='Run task',
                crontab=self.crontab,
                interval=self.interval,
                solar=self.solar,
                clocked=self.clocked,
                one_off=self.one_off,
                start_time=self.start_time,
            )
        debug_periodic_task.validate_unique()

    def create_periodic_task(self):
        logger.debug('Create periodic task')
        if not self.periodic_task:
            self.periodic_task = PeriodicTask(
                name=f"Croncierge Task {self.id}",
                task='Run task',
                args=f"[{self.id}]",
                crontab=self.crontab,
                interval=self.interval,
                solar=self.solar,
                clocked=self.clocked,
                one_off=self.one_off,
                start_time=self.start_time,
                enabled=self.enabled,
            )
            logger.debug('Pt: %s', self.periodic_task)
            self.periodic_task.save()
            self.save()

    def update_periodic_task(self):
        self.periodic_task.crontab = self.crontab
        self.periodic_task.interval = self.interval
        self.periodic_task.solar = self.solar
        self.periodic_task.clocked = self.clocked
        self.periodic_task.one_off = self.one_off
        self.periodic_task.start_time = self.start_time
        self.periodic_task.enabled = self.enabled        
        self.periodic_task.save()

    @classmethod
    def after_save(cls, instance, **kwargs):
        logger.info("After save: %s", kwargs)
        if not instance.periodic_task:
            instance.create_periodic_task()
        else:
            instance.update_periodic_task()

    def validate_unique(self, *args, **kwargs) -> None:
        self.validate_periodic_task(*args, **kwargs)
        return super().validate_unique(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)


    def __str__(self):
        return f"<Task (id{self.id}): {self.command[:15]}>"

signals.post_save.connect(Task.after_save, sender=Task)


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
