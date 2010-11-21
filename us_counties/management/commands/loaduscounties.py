from django.core.management.base import BaseCommand, CommandError
from us_counties import load

class Command(BaseCommand):
    help = 'Loads data for pluggable maps of U.S. counties'

    def handle(self, *args, **options):
        self.stdout.write('Loading data for U.S. counties\n')
        load.all()
        self.stdout.write('Successfully loaded data for U.S. counties\n')
