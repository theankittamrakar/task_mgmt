# Generated by Django 5.0 on 2023-12-31 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0004_rename_project_id_tasks_project_alter_teams_projects_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='user_name',
        ),
    ]
