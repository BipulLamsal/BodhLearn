# Generated by Django 4.1.3 on 2023-01-11 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_point"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="point",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
