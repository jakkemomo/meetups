# Generated by Django 4.2.3 on 2023-11-27 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('profiles', '0004_url_field_instead_of_image_field'), ('profiles', '0005_renamed_image_and_avatar_fields'), ('profiles', '0006_imagedields_to_charfields')]

    dependencies = [
        ('profiles', '0003_alter_user_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='avatar',
            new_name='avatar_url',
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.URLField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]