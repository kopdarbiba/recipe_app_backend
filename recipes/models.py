from django.db import models
from django.core.validators import MinValueValidator

from recipes.utils.s3_utils import create_presigned_url, delete_from_s3
from recipes.utils.thumbnail_utils import manage_thumbnails

from django.utils import timezone


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
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)], null=True)

    def __str__(self) -> str:
        return f"{self.name_en} | {self.name_lv} | {self.price}"

class Recipe(models.Model):
    cooking_time = models.PositiveIntegerField()
    servings = models.PositiveIntegerField()

    title = models.OneToOneField(Title, on_delete=models.SET_NULL, null=True)
    description = models.OneToOneField(Description, on_delete=models.SET_NULL, null=True)
    
    cuisines = models.ManyToManyField(Cuisine)
    occasions = models.ManyToManyField(Occasion)
    meals = models.ManyToManyField(Meal)
    dietary_preferences = models.ManyToManyField(DietaryPreference)
    equipment = models.ManyToManyField(Equipment)
    cooking_methods = models.ManyToManyField(CookingMethod, blank=True)
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    
    def __str__(self) -> str:
        return f"model Recipe: {self.title}"
   
    @property
    def total_price(self):
        # Access prefetched related recipe ingredients
        ingredients_sum = sum(
            ingredient.quantity * ingredient.ingredient.price for ingredient in self.recipe_ingredients.all()
        )

        return ingredients_sum   
  
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_time = timezone.now()
        self.modified_time = timezone.now()       
        super().save(*args, **kwargs)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.ingredient.name_en}"

class CookingStepInstruction(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='instructions')
    step_number = models.PositiveIntegerField(null=True, blank=True)
    name_lv = models.CharField(max_length=3000, null=True, blank=True)
    name_en = models.CharField(max_length=3000, null=True, blank=True)
    name_ru = models.CharField(max_length=3000, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name_en}"

    def save(self, *args, **kwargs):
        if not self.step_number:
            # Set step_number based on the count of instructions for the specific recipe
            self.step_number = CookingStepInstruction.objects.filter(recipe=self.recipe).count() + 1
        super().save(*args, **kwargs)
    
class RecipeImage(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='recipe_images/originals/')
    thumbnail = models.ImageField(upload_to='recipe_images/thumbnails/', null=True, blank=True, editable=False)
    is_main_image = models.BooleanField(default=False)

    class Meta:
        # Ensure there's only one image per recipe with is_main_image=True
        constraints = [
            models.UniqueConstraint(fields=['recipe'], condition=models.Q(is_main_image=True), name='unique_main_image')
        ]
    
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
        

    def __set_main_image(self):
        """This method ensures that there is one and only main image per reciepe. 
        If there is no main image, the one that is being currently uploaded is set to main.
        """
        existing_main_image = RecipeImage.objects.filter(recipe=self.recipe, is_main_image=True).exclude(id=self.id)
        if self.is_main_image:
            # If another main image exists, unset it
            if existing_main_image.exists():
                existing_main_image.update(is_main_image=False)
        else:
            # If there is no main image at all, the uploaded one will be set to main
            if not existing_main_image.exists():
               self.is_main_image = True 


    def save(self, *args, **kwargs):
        self.__set_main_image()
        super().save(*args, **kwargs)  # Call the original save method

        # Generate and save the thumbnail if the image has been changed
        manage_thumbnails(self)



