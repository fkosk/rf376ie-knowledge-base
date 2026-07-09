from django.core.management.base import BaseCommand
from fish_list.models import Base


class Command(BaseCommand):
    help = 'Import base names and translations from World.txt'

    def handle(self, *args, **kwargs):
        self.stdout.write('Importing bases from World.txt...')

        try:
            with open('World.txt', 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('World.txt not found!'))
            return

        lines = content.strip().split('\n')
        created = 0
        skipped = 0

        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split(':')
            if len(parts) < 2:
                continue

            dev_name = parts[0].strip()
            russian_name = parts[1].strip()

            _, was_created = Base.objects.update_or_create(
                dev_name=dev_name,
                defaults={'russian_name': russian_name}
            )

            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f'Import complete! Created: {created}, Updated: {skipped}'
        ))