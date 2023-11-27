from django.db import models

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=150)
    instructions = models.TextField(blank=True, null=True) # can be removed later
    servings = models.IntegerField(default=1)

    # # Basic info
    # description = models.TextField()
    # cuisine = models.CharField(max_length=50)
    # meal = models.CharField(max_length=50)
    # food_category = models.CharField(max_length=50)


    # # Details
    # cooking_time = models.IntegerField(default=0)
    # equipment = models.TextField(blank=True, null=True)
    # ingredient = models.TextField()
    # cooking_steps = models.TextField()
    # allergens = models.TextField(blank=True, null=True)
    # ingredient_substitude = models.TextField(blank=True, null=True)

    # # Nutrition
    # nutritional_info = models.TextField(blank=True, null=True)
    # calories = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)

    # # Rating
    # rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    # # Additional info
    # dietary_preference = models.CharField(max_length=50, blank=True, null=True)
    # measurements = models.DecimalField(max_digits=3, decimal_places=1, default=1)

    # # Date and Time
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)




 