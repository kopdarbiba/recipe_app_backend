# Recipe application
This is a repository of the recipe application's backend, created with Django and Django REST Framework.
The project is in the development.

## Endpoints
### /recipes/

Returns a list of all the recipes.
Following GET parameters are accepted:

**lang**
- lang=lv
- lang=ru
- lang=en

### /recipes/search/

Returns a filtered list of recipes.
Following GET parameters are accepted:

**lang**
- lang=lv
- lang=ru
- lang=en

**ordering**
- ordering=recipe_price  
   *(order by the prices of the recipes, ASC)*
- ordering=-recipe_price  
   *(order by the prices of the recipes, DESC)* 
- ordering=servings  
   *(order the recipes by the number of servings, ASC)* 
- ordering=-servings  
   *(order the recipes by the number of servings, DESC)* 
- ordering=cooking_time  
   *(order by the cooking time of the recipes, ASC)* 
- ordering=-cooking_time  
   *(order by the cooking time of the recipes, DESC)* 

**q**
- any string of text  
   *(for the recipes that contain that string of text in title or description)* 

**min_price**
- any decimal number  
   *(filter recipes with the prices that are higher or equal to the given number)* 

**max_price**
- any decimal number  
   *(filter recipes with the prices that are lower or equal to the given number)* 

**occasions (separated by comma)**

**meals**

**cuisines**

**ingredients**

### /recipes/{id}/
Returns a recipe details.
Following GET parameters are accepted:

**lang**
- lang=lv
- lang=ru
- lang=en

---
## Contributors
#### Developer Team
* Toms Tērauds
* Anta Osina
* Nadija Rubina
