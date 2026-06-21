from django.core.management.base import BaseCommand
from fish_list.models import Bait

class Command(BaseCommand):
    help = 'Populate database with bait translation data from baits.txt'

    def handle(self, *args, **kwargs):
        self.stdout.write('Пополняем базу данных наживками...')

        try:
            with open('baits.txt', 'r', encoding='utf-8') as f:

                created_count = 0
                updated_count = 0

                for line in f.readlines():
                    dev_name, russian_name = line.split(' : ')

                    bait_obj, created = Bait.objects.get_or_create(
                        dev_name=dev_name,
                        russian_name=russian_name
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                self.stdout.write(self.style.SUCCESS(
                    f'Успешно! Записей создано: {created_count}, Обновлено: {updated_count}'
                ))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                'Ошибка: baits.txt не найден! Убедитесь, что файл находится в одной директории с manage.py'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))