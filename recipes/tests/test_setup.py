from recipes.models import Cuisine, Meal, Occasion, Recipe, Description, Title, Ingredient, RecipeIngredient, Unit, DietaryPreference, Equipment, IngredientCategory, Allergen, CookingMethod, Adjective, CookingStepInstruction


def create_test_data():

    # Create titles for the test recipe
    t1 = Title.objects.create(name_en='title_1')
    t2 = Title.objects.create(name_en='title_2')
    t3 = Title.objects.create(name_en='title_3')

    # Create descriptions for the test recipe
    d1 = Description.objects.create(name_en='Description_1')
    d2 = Description.objects.create(name_en='Description_2')
    d3 = Description.objects.create(name_en='Description_3')

    # Create cuisines for the test recipe
    c1 = Cuisine.objects.create(name_en='Chinese', name_ru='Китайский', name_lv='Ķīniešu')
    c2 = Cuisine.objects.create(name_en='Indian', name_ru='Индийский', name_lv='Indijas')
    c3 = Cuisine.objects.create(name_en='Italian', name_ru='Итальянский', name_lv='Itālijs')

    # Create occasions for the test recipe
    o1 = Occasion.objects.create(name_en='Christmas', name_ru='Рождество', name_lv='Ziemassvētki')
    o2 = Occasion.objects.create(name_en='Birthday', name_ru='День рождения', name_lv='Dzimšanasdiena')
    o3 = Occasion.objects.create(name_en='Winter', name_ru='Зима', name_lv='Ziema')

    # Create meals for the test recipe
    m1 = Meal.objects.create(name_en='Breakfast', name_ru='Завтрак', name_lv='Brokastis')
    m2 = Meal.objects.create(name_en='Lunch', name_ru='Обед', name_lv='Pusdienas')
    m3 = Meal.objects.create(name_en='Dinner', name_ru='Ужин', name_lv='Vakariņas')

    # Create equipments for the test recipe
    e1 = Equipment.objects.create(name_en='Oven', name_ru='Горячая вода', name_lv='Plīts')
    e2 = Equipment.objects.create(name_en='Fridge', name_ru='Холодильник', name_lv='Ledusskapis')
    e3 = Equipment.objects.create(name_en='Spoon', name_ru='Ложка', name_lv='Karote')

    # Create dietary preferences for the test recipe
    dp1 = DietaryPreference.objects.create(name_en='Vegetarian', name_ru='Вегетарианский', name_lv='Vegetāris')
    dp2 = DietaryPreference.objects.create(name_en='Vegan', name_ru='Веганский', name_lv='Vegāns')
    dp3 = DietaryPreference.objects.create(name_en='Gluten-free', name_ru='Без глютена', name_lv='Bez glūtena')

    # Create ingredient categories for the test ingredients
    ic1 = IngredientCategory.objects.create(name_en='Protein', name_ru='Белки', name_lv='Protešu')
    ic2 = IngredientCategory.objects.create(name_en='Carbohydrates', name_ru='Жиры', name_lv='Karbohidru')
    ic3 = IngredientCategory.objects.create(name_en='Fat', name_ru='Углеводы', name_lv='Sodu')

    # Create allergens for the test ingredients
    a1 = Allergen.objects.create(name_en='Soy', name_ru='Соя', name_lv='Soja')
    a2 = Allergen.objects.create(name_en='Milk', name_ru='Молоко', name_lv='Piens')
    a3 = Allergen.objects.create(name_en='Eggs', name_ru='Яйца', name_lv='Olas')

    # Create cooking methods for the test recipe
    cm1 = CookingMethod.objects.create(name_en='Bake', name_ru='Готовить', name_lv='Gatavot')
    cm2 = CookingMethod.objects.create(name_en='Fry', name_ru='Жарить', name_lv='Cept')
    cm3 = CookingMethod.objects.create(name_en='Boil', name_ru='Кожа', name_lv='Vārīt')

    # Create units for the test ingredients
    u1 = Unit.objects.create(name_en='kg', name_ru='kg', name_lv='kg')
    u2 = Unit.objects.create(name_en='gab', name_ru='gab', name_lv='gab')
    u3 = Unit.objects.create(name_en='ml', name_ru='ml', name_lv='ml')
    u4 = Unit.objects.create(name_en='l', name_ru='l', name_lv='l')

    # Create adjectives for the test recipe
    ad1 = Adjective.objects.create(name_en='Easy', name_ru='Легкий', name_lv='Viegls')
    ad2 = Adjective.objects.create(name_en='Difficult', name_ru='Сложный', name_lv='Grūts')
    ad3 = Adjective.objects.create(name_en='Intermediate', name_ru='Средний', name_lv='Vidējs')

    # Create ingredients for the test recipe
    i1 = Ingredient.objects.create(name_en='Garlic', name_ru='Чеснок', name_lv='Ķiploks', price=3)
    i2 = Ingredient.objects.create(name_en='Apple', name_ru='Яблоко', name_lv='Ābols', price=6)
    i3 = Ingredient.objects.create(name_en='Salt', name_ru='Соль', name_lv='Sāls', price=100)
    i4 = Ingredient.objects.create(name_en='Pepper', name_ru='Перец', name_lv='Pipars', price=50)
    i5 = Ingredient.objects.create(name_en='Tomato', name_ru='Помидор', name_lv='Tomāts', price=10)
    i6 = Ingredient.objects.create(name_en='Onion', name_ru='Лук', name_lv='Sīpols', price=20)


    r1 = Recipe.objects.create(
        title=t1, 
        description=d1, 
        cuisine=c1, 
        occasion=o1,
        meal=m1,
        cooking_time=10, 
        servings=2, 
        )
    
    r1.dietary_preferences.set([dp1, dp2, dp3])
    r1.equipment.set([e1, e2])
    r1.cooking_methods.set([cm1, cm2])

    r2 = Recipe.objects.create(
        title=t2, 
        description=d2, 
        cuisine=c2,
        occasion=o2,
        meal=m2,
        cooking_time=20, 
        servings=4,
        )
    r2.dietary_preferences.set([dp1])
    r2.equipment.set([e3])
    r2.cooking_methods.set([cm3])

    r3 = Recipe.objects.create(
        title=t3,
        description=d3,
        cuisine=c3,
        occasion=o3,
        meal=m3, 
        cooking_time=30, 
        servings=6,
        )
    r3.dietary_preferences.set([dp3])
    r3.equipment.set([e1, e2])
    r3.cooking_methods.set([cm1, cm2])

    # Create RecipeIngredient instances for the test recipes with associated units and ingredients
    RecipeIngredient.objects.create(recipe=r1, ingredient=i1, quantity=1, unit=u1)
    RecipeIngredient.objects.create(recipe=r1, ingredient=i2, quantity=3, unit=u2)
    RecipeIngredient.objects.create(recipe=r2, ingredient=i3, quantity=13, unit=u3)
    RecipeIngredient.objects.create(recipe=r2, ingredient=i4, quantity=24, unit=u4)
    RecipeIngredient.objects.create(recipe=r3, ingredient=i5, quantity=5, unit=u1)
    RecipeIngredient.objects.create(recipe=r3, ingredient=i1, quantity=3, unit=u2)
    RecipeIngredient.objects.create(recipe=r3, ingredient=i2, quantity=7, unit=u3)

    # Create cooking step instructions for the test recipe
    cs1 = CookingStepInstruction.objects.create(recipe=r1, step_number=1, name_en='Cook the garlic and apple together.')
    cs2 = CookingStepInstruction.objects.create(recipe=r1, step_number=2, name_en='Add the salt and pepper.')
    cs3 = CookingStepInstruction.objects.create(recipe=r1, step_number=3, name_en='Serve the dish.')

