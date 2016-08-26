
import os
import os.path

from django.core.management.base import BaseCommand, CommandError

from dixit import settings
from dixit.game.models import Card


SUPPORTED_FORMATS = {
    '.jpg', '.jpeg', '.png', '.webp'
}


class Command(BaseCommand):
    """
    Register new cards in the database and purge missing ones
    """

    help = 'Scans the card directory and syncs available cards'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path', '-p',
            dest='path',
            help='Image path'
        )

    def handle(self, *args, **options):
        path = options.get('path') or settings.CARD_IMAGES_PATH
        path = os.path.realpath(path)

        if not os.path.exists(path):
            raise CommandError('Image path does not exist')

        def check_extension(f):
            f = f.lower()
            return f[f.rfind('.'):] in SUPPORTED_FORMATS

        for *_, files in os.walk(path):
            available = set(filter(check_extension, files))
            registered = {c.path for c in Card.objects.all()}

            Card.objects.exclude(path__in=available).delete()
            for path in available.difference(registered):
                Card(path=path).save()
