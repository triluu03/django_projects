# Generated by Django 4.1.3 on 2023-11-05 07:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tic_tac_toe", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="board",
            name="details",
            field=models.TextField(
                default=",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"
            ),
        ),
    ]