# Generated by Django 3.2.25 on 2025-01-23 16:35

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='image',
            field=models.ImageField(null=True, upload_to=core.models.activity_image_file_path),
        ),
    ]
