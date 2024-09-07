# Generated by Django 4.2.3 on 2024-09-07 07:34

import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("chats", "0003_message_read_at_message_status")]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="status",
            field=models.CharField(
                choices=[("unread", "Unread"), ("read", "Read"), ("deleted", "Deleted")],
                default="unread",
                max_length=32,
                verbose_name="Status",
            ),
        ),
        migrations.AddIndex(
            model_name="message",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["message_text"], name="trigram_text_idx", opclasses=["gin_trgm_ops"]
            ),
        ),
    ]
