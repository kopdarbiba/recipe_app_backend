from data_population.helpers import get_sheet_data_as_dict
from data_population.models import Ingridient
from django.core.management.base import BaseCommand


def db_populate(sheet_data_dict: dict) -> None:
    for row in sheet_data_dict:
        ingredient = Ingridient(title=row['title'], nosaukums=row['nosaukums'], calories=row['calories'])
        ingredient.save()

class Command(BaseCommand):
    help = 'Populate Ingridient objects'

    def handle(self, *args, **options):
        # Example usage:
        sheet_name = 'ingridient'
        relative_key_path = 'data_population/recipeapp.json'

        sheet_data_dict = get_sheet_data_as_dict(sheet_name, relative_key_path)

        if sheet_data_dict is None:
            print("Failed to retrieve sheet data.")
        else:
            db_populate(sheet_data_dict)

        self.stdout.write(self.style.SUCCESS('Ingridient objects have been successfully created and saved.'))
