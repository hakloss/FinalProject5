# Generated by Django 3.2 on 2021-04-26 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scheduler', '0006_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(default='empty', max_length=30)),
                ('section', models.IntegerField(default='empty', max_length=3)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='empty', max_length=254),
        ),
    ]
