from django.core.management.base import BaseCommand

from foodgram.models import Ingredient
import csv
from pathlib import Path
import logging


logging.basicConfig(filename='default.log')


class Command(BaseCommand):
    help = 'Load data from csv'

    def handle(self, *args, **options):
        path_to_dir = f'{Path(__file__).resolve().parent.parent.parent}'
        final_path = path_to_dir + '/data/ingredients.csv'
        with open(final_path) as csv_file:
            file_reader = csv.reader(csv_file)
            for row in file_reader:
                title, unit = row
                Ingredient.objects.get_or_create(title=title, unit=unit)
        logging.info(f'Добавлено {Ingredient.objects.count()} игредиентов')
