# Generated by Django 4.2.9 on 2024-06-06 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0001_initial"),
        ("leave", "0004_remove_leave_department"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leave",
            name="employee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="employee.employee"
            ),
        ),
    ]
