# Generated by Django 5.0.3 on 2024-04-03 08:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_recipe_created_time_recipe_modified_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 3, 8, 11, 24, 488191, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 3, 8, 11, 24, 488191, tzinfo=datetime.timezone.utc)),
        ),
    ]