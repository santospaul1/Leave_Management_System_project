# Generated by Django 4.2.9 on 2024-06-07 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leave", "0007_leave_days"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leave", name="days", field=models.IntegerField(default=0),
        ),
    ]
