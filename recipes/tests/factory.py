import factory
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
