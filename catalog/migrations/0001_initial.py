# Generated by Django 4.2.7 on 2023-11-30 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allergen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(max_length=255, unique=True)),
                ('name_lv', models.CharField(max_length=255, unique=True)),
                ('name_rus', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(max_length=255, unique=True)),
                ('name_lv', models.CharField(max_length=255, unique=True)),
                ('name_rus', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DietaryPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(max_length=255, unique=True)),
                ('name_lv', models.CharField(max_length=255, unique=True)),
                ('name_rus', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(max_length=255, unique=True)),
                ('name_lv', models.CharField(max_length=255, unique=True)),
                ('name_rus', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(max_length=255, unique=True)),
                ('name_lv', models.CharField(max_length=255, unique=True)),
                ('name_rus', models.CharField(max_length=255, unique=True)),
                ('allergens', models.ManyToManyField(blank=True, to='catalog.allergen')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(max_length=255, unique=True)),
                ('name_lv', models.CharField(max_length=255, unique=True)),
                ('name_rus', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(max_length=255, unique=True)),
                ('name_lv', models.CharField(max_length=255, unique=True)),
                ('name_rus', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('cooking_time', models.PositiveIntegerField()),
                ('servings', models.PositiveIntegerField()),
                ('instructions', models.TextField()),
                ('nutritional_information', models.JSONField()),
                ('cuisine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.cuisine')),
                ('dietary_preferences', models.ManyToManyField(to='catalog.dietarypreference')),
                ('equipment', models.ManyToManyField(to='catalog.equipment')),
                ('ingredient_substitutes', models.ManyToManyField(blank=True, related_name='substitutes', to='catalog.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(max_length=255, unique=True)),
                ('name_lv', models.CharField(max_length=255, unique=True)),
                ('name_rus', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=50)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.recipe')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.unit')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='catalog.RecipeIngredient', to='catalog.ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='meal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.meal'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.ingredientcategory'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='units',
            field=models.ManyToManyField(blank=True, to='catalog.unit'),
        ),
    ]
