# Generated by Django 3.2 on 2021-04-28 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scheduler', '0012_alter_section_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='classname',
            field=models.CharField(blank=True, default='empty', max_length=30, null=True),
        ),
    ]
