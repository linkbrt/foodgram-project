from django.core.management.base import BaseCommand, CommandError

from foodgram.models import Ingredient
import csv, os
from pathlib import Path


class Command(BaseCommand):
    help = 'Load data from csv'

    def handle(self, *args, **options):
        path_to_csv = f'{Path(__file__).resolve().parent.parent.parent} \
                       /data/ingredients.csv'
        with open(path_to_csv) as csv_file:
            file_reader = csv.reader(csv_file)
            for row in file_reader:
                title, unit = row
                Ingredient.objects.get_or_create(title=title, unit=unit)
        print(f'Добавлено {Ingredient.objects.count()} игредиентов')
