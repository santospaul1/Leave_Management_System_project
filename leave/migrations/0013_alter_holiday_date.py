# Generated by Django 4.2.9 on 2024-06-10 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leave", "0012_holiday"),
    ]

    operations = [
        migrations.AlterField(
            model_name="holiday", name="date", field=models.DateField(unique=True),
        ),
    ]
