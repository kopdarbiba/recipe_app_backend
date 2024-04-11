from factory.django import DjangoModelFactory as DMF
import factory
from factory import SubFactory, Faker, post_generation, fuzzy
from ..models import Recipe, RecipeIngredient, Title, Description, Cuisine, Occasion, Meal, DietaryPreference, Equipment, CookingMethod, IngredientCategory, Allergen, CookingMethod, Unit, Ingredient

class TitleFactory(DMF):
    class Meta:
        model = Title

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class DescriptionFactory(DMF):
    class Meta:
        model = Description

    name_en = Faker('text', max_nb_chars=3000)
    name_lv = Faker('text', max_nb_chars=3000, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=3000, locale='ru_RU')

class CuisineFactory(DMF):
    class Meta:
        model = Cuisine

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class OccasionFactory(DMF):
    class Meta:
        model = Occasion

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class MealFactory(DMF):
    class Meta:
        model = Meal

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class EquipmentFactory(DMF):
    class Meta:
        model = Equipment

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class DietaryPreferenceFactory(DMF):
    class Meta:
        model = DietaryPreference

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class IngredientCategoryFactory(DMF):
    class Meta:
        model = IngredientCategory

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class AllergenFactory(DMF):
    class Meta:
        model = Allergen

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class CookingMethodFactory(DMF):
    class Meta:
        model = CookingMethod

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')

class UnitFactory(DMF):
    class Meta:
        model = Unit

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')
    type_shoping_valid = Faker('boolean')

class IngredientFactory(DMF):
    class Meta:
        model = Ingredient

    allergen = SubFactory(AllergenFactory)
    category = SubFactory(IngredientCategoryFactory)

    name_en = Faker('text', max_nb_chars=255)
    name_lv = Faker('text', max_nb_chars=255, locale='lv_LV')
    name_ru = Faker('text', max_nb_chars=255, locale='ru_RU')
    price = fuzzy.FuzzyDecimal(0.5, 42.7, precision=2)

class RecipeFactory(DMF):
    class Meta:
        model = Recipe

    title = SubFactory(TitleFactory)
    description = SubFactory(DescriptionFactory)

    # Other fields
    cooking_time = Faker('random_int', min=10, max=120)
    servings = Faker('random_int', min=1, max=10)
    created_time = Faker('date_object')
    modified_time = Faker('date_object')
    

    # ManyToMany fields
    @post_generation
    def cuisines(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for cuisine in extracted:
                self.cuisines.add(cuisine)

    @post_generation
    def occasions(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for occasion in extracted:
                self.occasions.add(occasion)

    @post_generation
    def meals(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for meal in extracted:
                self.meals.add(meal)

    @post_generation
    def dietary_preferences(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for dietary_preference in extracted:
                self.dietary_preferences.add(dietary_preference)

    @post_generation
    def equipment(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for equipment_instance in extracted:
                self.equipment.add(equipment_instance)

    @post_generation
    def cooking_methods(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for cooking_method_instance in extracted:
                self.cooking_methods.add(cooking_method_instance)


class RecipeIngredientFactory(DMF):
    class Meta:
        model = RecipeIngredient

    recipe = SubFactory(RecipeFactory)  # Assuming RecipeFactory is properly defined
    ingredient = SubFactory(IngredientFactory)  # Assuming IngredientFactory is properly defined
    quantity = fuzzy.FuzzyDecimal(0.1, 10.0, precision=2)
    unit = SubFactory(UnitFactory)  # Assuming UnitFactory is properly defined
