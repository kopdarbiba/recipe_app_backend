from data_population.helpers import get_sheet_data_as_dict
from data_population.manage_sheet_data import db_populate
from data_population.models import Ingridient
from django.core.management.base import BaseCommand




class Command(BaseCommand):
    help = 'Populate Ingridient objects'

    def handle(self, *args, **options):
        # Example usage:
        # sheet_name = 'ingridient'
        sheet_name = 'RecipeData'
        relative_key_path = 'data_population/recipeapp.json'

        sheet_data_dict = get_sheet_data_as_dict(sheet_name, relative_key_path)

        if sheet_data_dict is None:
            print("Failed to retrieve sheet data.")
        else:
            db_populate(sheet_data_dict)

        self.stdout.write(self.style.SUCCESS(f'{sheet_name} objects have been successfully created and saved.'))
