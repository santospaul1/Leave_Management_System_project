# Generated by Django 4.2.9 on 2024-06-22 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="images",
            field=models.ImageField(null=True, upload_to="images/"),
        ),
    ]