# Generated by Django 5.0 on 2024-01-03 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0006_attachments_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='is_current',
            field=models.BooleanField(default=True),
        ),
    ]
