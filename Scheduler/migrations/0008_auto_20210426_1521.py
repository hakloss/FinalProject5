# Generated by Django 3.2 on 2021-04-26 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scheduler', '0007_auto_20210426_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='course',
            new_name='classname',
        ),
        migrations.AlterField(
            model_name='course',
            name='section',
            field=models.IntegerField(default='empty'),
        ),
    ]
