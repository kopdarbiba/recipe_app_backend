# tests/factories.py
import io
from unittest.mock import patch
import factory
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import RecipeImage
from factory import Factory, SubFactory, Faker
from ..models import Recipe, Title, Description, Cuisine, Occasion, Meal, DietaryPreference, Equipment, CookingMethod, IngredientCategory, Allergen, CookingMethod, Unit, Ingredient

# Create factories for related models if needed
class TitleFactory(Factory):
    class Meta:
        model = Title

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class DescriptionFactory(Factory):
    class Meta:
        model = Description

    name_en = Faker('text', max_nb_chars=3000)
    name_lv = Faker('text', max_nb_chars=3000, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=3000, locale='ru_RU')

class CuisineFactory(Factory):
    class Meta:
        model = Cuisine

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class OccasionFactory(Factory):
    class Meta:
        model = Occasion

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class MealFactory(Factory):
    class Meta:
        model = Meal

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class EquipmentFactory(Factory):
    class Meta:
        model = Equipment

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class DietaryPreferenceFactory(Factory):
    class Meta:
        model = DietaryPreference

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class IngredientCategoryFactory(Factory):
    class Meta:
        model = IngredientCategory

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class AllergenFactory(Factory):
    class Meta:
        model = Allergen

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class CookingMethodFactory(Factory):
    class Meta:
        model = CookingMethod

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class UnitFactory(Factory):
    class Meta:
        model = Unit

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')
    type_shoping_valid = Faker('boolean')

class IngredientFactory(Factory):
    class Meta:
        model = Ingredient

    allergen = SubFactory(AllergenFactory)
    category = SubFactory(IngredientCategoryFactory)

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')
    price = Faker('random_decimal', left_digits=4, right_digits=2, positive=True)

class RecipeFactory(Factory):
    class Meta:
        model = Recipe

    # Use SubFactory to create related instances
    title = SubFactory(TitleFactory)
    description = SubFactory(DescriptionFactory)
    cuisine = SubFactory(CuisineFactory)
    occasion = SubFactory(OccasionFactory)
    meal = SubFactory(MealFactory)

    # Other fields
    cooking_time = Faker('random_int', min=10, max=120)
    servings = Faker('random_int', min=1, max=10)

    # ManyToMany fields
    @factory.post_generation
    def dietary_preferences(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for dietary_preference in extracted:
                self.dietary_preferences.add(dietary_preference)

    @factory.post_generation
    def equipment(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for equipment_instance in extracted:
                self.equipment.add(equipment_instance)

    @factory.post_generation
    def cooking_methods(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for cooking_method_instance in extracted:
                self.cooking_methods.add(cooking_method_instance)

    # Define a sequence for unique titles
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        title = kwargs.get('title') or f'Test Recipe {cls._meta.seq + 1}'
        kwargs['title'] = title
        return super()._create(model_class, *args, **kwargs)


# from factory import Factory, SubFactory, post_generation
# from PIL import Image, ImageOps
# from recipes.utils.thumbnail_utils import manage_thumbnails

# class RecipeImageFactory(Factory):
#     class Meta:
#         model = RecipeImage

#     recipe = SubFactory(RecipeFactory)
#     image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x00\x00\x00\x01\x00\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x03$IDATx\x9c\xec}\t\x94\xe3\xde9\xcfy\xe6\xf9\xf4\xc7\x1c\x87\x84\xbd\x1f\xd3\xb9?\xc9\xfc\x03\x00\x00\xf1zZY\x00\x00\x00\x00IEND\xaeB`\x82'
#     is_main_image = Faker('boolean')

#     @post_generation
#     def generate_thumbnail(self, create, extracted, **kwargs):
#         if not create:
#             return

#         try:
#             if self.image_content and not self.thumbnail:
#                 thumbnail = self.generate_thumbnail()

#                 # Save the thumbnail
#                 self.save_thumbnail(thumbnail)
#         except Exception as e:
#             print(f"Error in generate_thumbnail: {e}")

#     @post_generation
#     def generate_thumbnail(self):
#         try:
#             img = Image.open(io.BytesIO(self.image_content))

#             thumbnail_size = (100, 100)
#             thumbnail = ImageOps.fit(img, thumbnail_size)

#             return thumbnail
#         except Exception as e:
#             print(f"Error in generate_thumbnail: {e}")
#             return None

#     def save_thumbnail(self, thumbnail):
#         try:
#             # Save the thumbnail to the desired location
#             thumbnail_path = "recipe_images/thumbnails/"  # Adjust this based on your actual structure
#             thumbnail_name = f"{self.image.name.split('/')[-1].split('.')[0]}_thumbnail.jpg"
#             thumbnail_full_path = thumbnail_path + thumbnail_name
#             thumbnail.save(thumbnail_full_path, "JPEG")

#             # Update the thumbnail field in the RecipeImage model
#             self.thumbnail = thumbnail_full_path
#             self.save()
#         except Exception as e:
#             print(f"Error in save_thumbnail: {e}")
