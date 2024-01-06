import os
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from recipes.utils.utilities import create_presigned_url, delete_from_s3


class Title(models.Model):
    name_en = models.CharField(max_length=255)
    name_lv = models.CharField(max_length=255, null=True, blank=True)
    name_ru = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name_en}"

class Description(models.Model):
    name_en = models.TextField()
    name_lv = models.TextField(max_length=3000, null=True, blank=True)
    name_ru = models.TextField(max_length=3000, null=True, blank=True)

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

class Adjective(models.Model):
    name_en = models.CharField(max_length=50, unique=True)
    name_lv = models.CharField(max_length=50, unique=True)
    name_ru = models.CharField(max_length=50, unique=True)

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
        return f"{self.name_en} | {self.name_lv}"
    
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
    
    def get_price(self):
        total_price = 0

        for recipe_ingredient in self.recipe_ingredients.all():
            total_price += recipe_ingredient.quantity * recipe_ingredient.ingredient.price

        # If there are no ingredients, return 0
        return total_price or 0
        
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    # def check_positive_quantity(self):
    #     if self.quantity <= 0:
    #         raise ValidationError("Quantity must be positive.")
    #     return True

    def __str__(self):
        return f"{self.ingredient.name_en}:  {self.quantity} {self.unit}" 

class CookingStepInstruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions')
    step_number = models.PositiveSmallIntegerField()
    name_en = models.TextField(max_length=3000, null=True, blank=True)
    name_lv = models.TextField(max_length=3000, null=True, blank=True)
    name_ru = models.TextField(max_length=3000, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name_en}"
    
class CookingStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_number = models.PositiveSmallIntegerField()
    cooking_method = models.ForeignKey(CookingMethod, on_delete=models.CASCADE)
    recipe_ingredients = models.ManyToManyField(RecipeIngredient)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    adjective_cm = models.ManyToManyField(Adjective, blank=True, related_name='adjective_cm_set')
    adjective_ri = models.ManyToManyField(Adjective, blank=True, related_name='adjective_ri_set')
    adjective_alt = models.ManyToManyField(Adjective, blank=True, related_name='adjective_alt_set')
    
    def __str__(self) -> str:
        return f"Cooking Step for {self.recipe} - {self.cooking_method}"

class RecipeImage(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='recipe_images/originals/')
    thumbnail = models.ImageField(upload_to='recipe_images/thumbnails/', null=True, blank=True, editable=False)
    is_main_image = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image and not self.thumbnail:
            # Generate thumbnail asynchronously using a task queue (e.g., Celery)
            generate_thumbnail.delay(self.id, self.image.name)

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

@receiver(pre_delete, sender=RecipeImage)
def delete_s3_images(sender, instance, **kwargs):
    # This signal is triggered just before the model instance is deleted
    # You can use it to delete S3 objects associated with the instance
    s3_key_image = instance.image.name
    s3_key_thumbnail = instance.thumbnail.name if instance.thumbnail else None

    # Delete the original image and thumbnail
    delete_from_s3(s3_key_image)
    if s3_key_thumbnail:
        delete_from_s3(s3_key_thumbnail)

@receiver(models.signals.post_save, sender=RecipeImage)
def generate_thumbnail(sender, instance, **kwargs):
    # Generate thumbnail here and save it to the instance
    # This can be done asynchronously using a task queue like Celery
    if instance.image and not instance.thumbnail:
        # Open the original image using Pillow
        img = Image.open(instance.image)

        # Create a thumbnail
        thumbnail_size = (200, 200)  # Adjust the size as needed
        img.thumbnail(thumbnail_size)

        # Convert the image to RGB mode if it's in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Create an in-memory file
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG')

        # Save the thumbnail to the thumbnail field
        image_name = os.path.basename(instance.image.name)
        thumbnail_path = f"thumb_{image_name}"
        instance.thumbnail.save(
            thumbnail_path,
            InMemoryUploadedFile(
                thumb_io,
                None,
                thumbnail_path,
                'image/jpeg',
                thumb_io.tell,
                None
            )
        )
