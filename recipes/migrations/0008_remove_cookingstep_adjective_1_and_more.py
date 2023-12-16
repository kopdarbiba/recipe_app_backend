# Generated by Django 4.2.7 on 2023-12-16 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_remove_cookingstep_adjective_cookingstep_adjective_1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cookingstep',
            name='adjective_1',
        ),
        migrations.RemoveField(
            model_name='cookingstep',
            name='adjective_2',
        ),
        migrations.RemoveField(
            model_name='cookingstep',
            name='adjective_3',
        ),
        migrations.AddField(
            model_name='cookingstep',
            name='adjective_alt',
            field=models.ManyToManyField(blank=True, related_name='adjective_alt_set', to='recipes.adjective'),
        ),
        migrations.AddField(
            model_name='cookingstep',
            name='adjective_cm',
            field=models.ManyToManyField(blank=True, related_name='adjective_cm_set', to='recipes.adjective'),
        ),
        migrations.AddField(
            model_name='cookingstep',
            name='adjective_ri',
            field=models.ManyToManyField(blank=True, related_name='adjective_ri_set', to='recipes.adjective'),
        ),
    ]
