from django.db import models

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=150)
    instructions = models.TextField(blank=True, null=True)
    servings = models.DecimalField(max_digits=10, decimal_places=2, default=1.00 )
    