from django.core.management.base import BaseCommand
from fish_list.models import Pref


class Command(BaseCommand):
    help = 'Import spinning lure preferences from Pref.txt'

    def handle(self, *args, **kwargs):
        self.stdout.write('Importing Pref data...')

        try:
            with open('Pref.txt', 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Pref.txt not found!'))
            return

        # Split by base sections (### indicates new base)
        sections = content.strip().split('###')

        created = 0
        skipped = 0

        for section in sections:
            section = section.strip()
            if not section:
                continue

            lines = section.split('\n')
            base_name = lines[0].strip()

            self.stdout.write(f'Processing base: {base_name}')

            for line in lines[1:]:
                line = line.strip()
                if not line or line.startswith('---'):
                    continue

                # Parse fish_id:fish_name#lure1:value1:lure2:value2...
                try:
                    # Split fish info and lures
                    fish_part, lures_part = line.split('#', 1)

                    # Get fish_id and fish_name
                    fish_id, fish_name = fish_part.split(':', 1)

                    # Parse lures
                    lure_items = lures_part.split(':')
                    spinning_lures = {}

                    # Process pairs (name:value)
                    for i in range(0, len(lure_items), 2):
                        if i + 1 < len(lure_items):
                            lure_name = lure_items[i].strip()
                            lure_value = int(lure_items[i + 1].strip())
                            spinning_lures[lure_name] = lure_value

                    # Create or update
                    pref, was_created = Pref.objects.update_or_create(
                        base=base_name,
                        fish_id=fish_id,
                        defaults={
                            'fish_name': fish_name,
                            'spinning_lures': spinning_lures,
                        }
                    )

                    if was_created:
                        created += 1
                    else:
                        skipped += 1

                except (ValueError, IndexError) as e:
                    self.stdout.write(self.style.WARNING(
                        f'Skipping malformed line in {base_name}: {line[:50]}... ({str(e)})'
                    ))
                    continue

        self.stdout.write(self.style.SUCCESS(
            f'Import complete! Created: {created}, Updated: {skipped}'
        ))