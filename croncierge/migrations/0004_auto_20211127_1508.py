# Generated by Django 3.2.9 on 2021-11-27 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('croncierge', '0003_task__periodic_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='_periodic_task',
        ),
        migrations.AddField(
            model_name='task',
            name='periodic_task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='_periodic_task', to='django_celery_beat.periodictask'),
        ),
    ]
