# Generated by Django 4.2.3 on 2023-07-29 11:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("profiles", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True, default="users/image/default-user.jpeg", null=True, upload_to=None
            ),
        )
    ]
