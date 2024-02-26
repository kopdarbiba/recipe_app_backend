from django.db import models
from django.db.models import Sum, F
from django.core.validators import MinValueValidator

from recipes.utils.s3_utils import create_presigned_url, delete_from_s3
from recipes.utils.thumbnail_utils import manage_thumbnails


class Title(models.Model):
    name_en = models.CharField(max_length=255)
    name_lv = models.CharField(max_length=255, null=True, blank=True)
    name_ru = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name_en}"

class Description(models.Model):
    name_en = models.CharField(max_length=3000)
    name_lv = models.CharField(max_length=3000, null=True, blank=True)
    name_ru = models.CharField(max_length=3000, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name_en}"

class Cuisine(models.Model):
    name_en = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_en} | {self.name_lv}"
    
class Occasion(models.Model):
    name_en = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_en} | {self.name_lv}"

class Meal(models.Model):
    name_en = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_en} | {self.name_lv}"

class Equipment(models.Model):
    name_en = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_en} | {self.name_lv}"

class DietaryPreference(models.Model):
    name_en = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_en} | {self.name_lv}"
    
class IngredientCategory(models.Model):
    name_en = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_en} | {self.name_lv}"

class Allergen(models.Model):
    name_en = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_en} | {self.name_lv}"

class CookingMethod(models.Model):
    name_en = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name_en} | {self.name_lv}"

class Unit(models.Model):
    name_en = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)
    type_shoping_valid = models.BooleanField(null=True)

    def __str__(self) -> str:
        return f"{self.name_en} | {self.name_lv}"

class Ingredient(models.Model):
    allergen = models.ForeignKey(Allergen, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(IngredientCategory, on_delete=models.SET_NULL, null=True)

    name_en = models.CharField(max_length=255, unique=True)
    name_lv = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__(self) -> str:
        return f"{self.name_en} | {self.name_lv} | {self.price}"
    
class Recipe(models.Model):
    title = models.OneToOneField(Title, on_delete=models.SET_NULL, null=True)
    description = models.OneToOneField(Description, on_delete=models.SET_NULL, null=True)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True, blank=True)
    occasion = models.ForeignKey(Occasion, on_delete=models.SET_NULL, null=True, blank=True)
    meal = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True)
    cooking_time = models.PositiveIntegerField()
    servings = models.PositiveIntegerField()
    dietary_preferences = models.ManyToManyField(DietaryPreference)
    equipment = models.ManyToManyField(Equipment)
    cooking_methods = models.ManyToManyField(CookingMethod, blank=True)
    
    def __str__(self) -> str:
        return f"model Recipe: {self.title}"

    def get_recipe_total_price(self):
        # Calculate the total price based on quantity and ingredient's price
        total_price = self.recipe_ingredients.annotate(
            total_price_per_ingredient=F('quantity') * F('ingredient__price')
        ).aggregate(
            total_price=Sum('total_price_per_ingredient')
        )['total_price']

        # If there are no ingredients, return 0
        return total_price or 0

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.ingredient.name_en}: {self.calculate_price()}"
   
    # Returns calculated price (quantity x price)
    def calculate_price(self):
        return self.quantity * self.ingredient.price

class CookingStepInstruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions')
    step_number = models.PositiveSmallIntegerField()
    name_en = models.TextField(max_length=3000, null=True, blank=True)
    name_lv = models.TextField(max_length=3000, null=True, blank=True)
    name_ru = models.TextField(max_length=3000, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name_en}"
    
class RecipeImage(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='recipe_images/originals/')
    thumbnail = models.ImageField(upload_to='recipe_images/thumbnails/', null=True, blank=True, editable=False)
    is_main_image = models.BooleanField(default=False)

    def generate_presigned_url_for_image(self, expiration_time=3600):
        s3_key = self.image.name
        return create_presigned_url(s3_key, expiration_time)

    def generate_presigned_url_for_thumbnail(self, expiration_time=3600):
        s3_key = self.thumbnail.name
        return create_presigned_url(s3_key, expiration_time)

    def delete(self, *args, **kwargs):
        # Delete the image and thumbnail from S3 before removing the model instance
        s3_key_image = self.image.name
        s3_key_thumbnail = self.thumbnail.name if self.thumbnail else None

        # Delete the original image and thumbnail
        delete_from_s3(s3_key_image)
        if s3_key_thumbnail:
            delete_from_s3(s3_key_thumbnail)

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the original save method

        # Generate and save the thumbnail if the image has been changed
        manage_thumbnails(self)

