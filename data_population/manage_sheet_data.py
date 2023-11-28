from data_population.models import Ingridient


def db_populate(sheet_data_dict: dict) -> None:
    for row in sheet_data_dict:
        ingredient = Ingridient(title=row['title'], nosaukums=row['nosaukums'], calories=row['calories'])
        ingredient.save()