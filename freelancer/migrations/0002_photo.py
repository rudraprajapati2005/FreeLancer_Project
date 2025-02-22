# Generated by Django 5.1.4 on 2025-02-17 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("freelancer", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Photo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=255, unique=True)),
                ("image", models.ImageField(upload_to="photos/profile_pic")),
            ],
        ),
    ]
