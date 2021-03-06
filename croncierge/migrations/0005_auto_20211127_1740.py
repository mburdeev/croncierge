# Generated by Django 3.2.9 on 2021-11-27 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('croncierge', '0004_auto_20211127_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='clocked',
            field=models.ForeignKey(blank=True, help_text='Clocked Schedule to run the task on.  Set only one schedule type, leave the others null.', null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.clockedschedule', verbose_name='Clocked Schedule'),
        ),
        migrations.AddField(
            model_name='task',
            name='interval',
            field=models.ForeignKey(blank=True, help_text='Interval Schedule to run the task on.  Set only one schedule type, leave the others null.', null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.intervalschedule', verbose_name='Interval Schedule'),
        ),
        migrations.AddField(
            model_name='task',
            name='solar',
            field=models.ForeignKey(blank=True, help_text='Solar Schedule to run the task on.  Set only one schedule type, leave the others null.', null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.solarschedule', verbose_name='Solar Schedule'),
        ),
    ]
