# Generated by Django 5.0.6 on 2024-07-18 00:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("signup", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
