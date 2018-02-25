from django.core.management.base import BaseCommand, CommandError
from shortener.models import MashURL

class Command(BaseCommand):
    help = 'Refreshes all MashURL shortcodes'

    def add_arguments(self, parser):
        parser.add_argument('--items', type=int)

    def handle(self, *args, **options):
        return MashURL.objects.refresh_shortcodes(items=options['items'])
