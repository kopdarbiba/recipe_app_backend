# Generated by Django 4.2.7 on 2023-12-15 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_info', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookingmethod',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
