# Generated by Django 4.2.3 on 2024-01-03 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_remove_userrating_user_rater'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrating',
            name='updated_by',
        ),
    ]