"""
Django command to wait for databse to wait to be avaliable
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for databse"""

    def handle(self, *args, **options):
        """Entrypoint"""
        self.stdout.write("Waiting for database to be running...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("Database unavaliable, \
                                  waiting 1 second ....")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database avaliable'))
