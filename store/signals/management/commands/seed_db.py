from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Seed the database with initial data from seed.sql'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database from seed.sql...')
        
        sql_path = '/Users/ankushaggarwal/Code/storefront/store/signals/management/commands/seed.sql'
        with open(sql_path, 'r') as file:
            sql = file.read()
        
        with connection.cursor() as cursor:
            cursor.execute(sql)
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully from seed.sql!'))
