import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    """
    Django command for database waiting when app in startup mode.

    It prevent app to crash while starting service up when
    database not ready for connection.

    Args:
        BaseCommand (): Django inherited class for commands.
    """

    def handle(self, *args, **options):
        """
        Handle db checking.
        """
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (OperationalError, Psycopg2Error):
                time.sleep(1)
