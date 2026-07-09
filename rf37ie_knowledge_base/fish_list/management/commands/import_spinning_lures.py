from django.core.management.base import BaseCommand
from fish_list.models import SpinningLure


class Command(BaseCommand):
    help = 'Import spinning lure types from Spinning_lures.txt'

    def handle(self, *args, **kwargs):
        self.stdout.write('Importing spinning lure types...')

        try:
            with open('Spinning_lures.txt', 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Spinning_lures.txt not found!'))
            return

        lines = content.strip().split('\n')
        created = 0
        skipped = 0
        errors = 0

        for line in lines:
            line = line.strip()
            if not line:
                continue

            try:
                parts = line.split(':')

                if len(parts) < 3:
                    self.stdout.write(self.style.WARNING(
                        f'Skipping malformed line: {line[:50]}...'
                    ))
                    errors += 1
                    continue

                lure_name = parts[0].strip()
                lure_type = parts[2].strip()  # Third element is the type

                _, was_created = SpinningLure.objects.update_or_create(
                    lure_name=lure_name,
                    defaults={'lure_type': lure_type}
                )

                if was_created:
                    created += 1
                else:
                    skipped += 1

            except (ValueError, IndexError) as e:
                self.stdout.write(self.style.WARNING(
                    f'Skipping line: {line[:50]}... ({str(e)})'
                ))
                errors += 1

        self.stdout.write(self.style.SUCCESS(
            f'Import complete! Created: {created}, Updated: {skipped}, Errors: {errors}'
        ))