from django.db import models

# Create your models here.
class RecipeGeneralInfo(models.Model):
    title = models.CharField(max_length=255)
    cooking_time = models.PositiveIntegerField()  # in minutes
    servings = models.PositiveIntegerField()
    description = models.TextField()
    nutritional_information = models.JSONField()
    
    def __str__(self) -> str:
        return f"{self.title}"