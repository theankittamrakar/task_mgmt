# Generated by Django 5.0 on 2023-12-31 05:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task_app.departments'),
        ),
    ]
