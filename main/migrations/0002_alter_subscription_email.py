# Generated by Django 3.2.5 on 2021-08-05 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
