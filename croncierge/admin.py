from django.contrib import admin

from croncierge.models import (
    Task, Log
)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['command']

    # def save_model(self, request, obj, form, change):
    #     obj.save(form=form)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = [
        'task','stdout','stderr','status_code',
        'started_at','exited_at',]


