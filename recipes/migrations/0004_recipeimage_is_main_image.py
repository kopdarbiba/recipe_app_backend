# Generated by Django 4.2.7 on 2024-01-02 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_recipeimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeimage',
            name='is_main_image',
            field=models.BooleanField(default=False),
        ),
    ]