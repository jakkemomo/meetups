# Generated by Django 4.2.3 on 2023-12-21 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("profiles", "0007_user_is_email_verified")]

    operations = [
        migrations.RenameField(model_name="user", old_name="avatar_url", new_name="image_url")
    ]
