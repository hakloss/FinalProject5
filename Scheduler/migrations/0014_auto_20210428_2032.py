# Generated by Django 3.2 on 2021-04-28 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scheduler', '0013_alter_course_classname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='number',
            field=models.CharField(blank=True, default='empty', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='time',
            field=models.CharField(blank=True, default='empty', max_length=40, null=True),
        ),
    ]

