# Generated by Django 4.2.3 on 2024-06-06 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0022_citylocation_citylocation_unique_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citylocation',
            name='place_id',
            field=models.CharField(default=None, max_length=255, null=True, unique=True),
        ),
    ]
