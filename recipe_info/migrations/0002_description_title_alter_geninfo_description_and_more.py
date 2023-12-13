# Generated by Django 4.2.7 on 2023-12-13 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.TextField(max_length=3000)),
                ('name_lv', models.TextField(max_length=3000, null=True)),
                ('name_rus', models.TextField(max_length=3000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(max_length=255)),
                ('name_lv', models.CharField(max_length=255, null=True)),
                ('name_rus', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='geninfo',
            name='description',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipe_info.description'),
        ),
        migrations.AlterField(
            model_name='geninfo',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipe_info.title'),
        ),
    ]
