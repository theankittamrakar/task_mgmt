# Generated by Django 5.0 on 2023-12-31 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0002_alter_users_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='permissions',
        ),
        migrations.RemoveField(
            model_name='users',
            name='roles',
        ),
        migrations.DeleteModel(
            name='Permissions',
        ),
        migrations.DeleteModel(
            name='Roles',
        ),
    ]