# Generated by Django 3.2.5 on 2021-09-13 13:16

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_emailrecord"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="unsubscribe_key",
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]
