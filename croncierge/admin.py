from django.contrib import admin

from croncierge.models import (
    Task, Log
)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['command']


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = [
        'task','stdout','stderr','status_code',
        'started_at','exited_at',]


