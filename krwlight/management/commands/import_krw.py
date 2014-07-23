# Used to automatically book 40 hours on an internal project for managers.
import logging

from django.core.management.base import BaseCommand

from krwlight import data

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ""
    help = "Import the demo .csv files"

    def handle(self, *args, **options):
        import pprint
        pprint.pprint(data.location_tree())
