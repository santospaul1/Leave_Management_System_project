# Generated by Django 4.2.9 on 2024-07-04 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feedback", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedback",
            name="sentiment_polarity",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="feedback",
            name="sentiment_subjectivity",
            field=models.FloatField(blank=True, null=True),
        ),
    ]