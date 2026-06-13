import json
from django.core.management.base import BaseCommand
from fish_list.models import Fish


def ensure_list(value):
    if isinstance(value, list):
        return value
    else:
        return [value]


class Command(BaseCommand):
    help = 'Populate database with fish data from fish_data_v3.json'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database population...')

        try:
            with open('fish_data_v3.json', 'r', encoding='utf-8') as f:
                fish_dict = json.load(f)

            created_count = 0
            updated_count = 0

            for fish_key in fish_dict:
                fish_data = fish_dict[fish_key]

                # Use update_or_create to avoid duplicates
                fish_obj, created = Fish.objects.update_or_create(
                    id=fish_data["Код рыбы"],
                    defaults={
                        'name': fish_data["Вид"]["Именительный"],
                        'min_weight': fish_data["Минимальный вес"],
                        'max_weight': fish_data["Максимальный вес"],
                        'min_depth_small': fish_data["Минимальная глубина"]["Маленькая"],
                        'min_depth_medium': fish_data["Минимальная глубина"]["Средняя"],
                        'min_depth_large': fish_data["Минимальная глубина"]["Большая"],
                        'amount_on_bottom_small': fish_data["Предпочитаемая глубина"]["По дну"]["Маленькая"],
                        'amount_on_bottom_medium': fish_data["Предпочитаемая глубина"]["По дну"]["Средняя"],
                        'amount_on_bottom_large': fish_data["Предпочитаемая глубина"]["По дну"]["Большая"],
                        'amount_on_middle_small': fish_data["Предпочитаемая глубина"]["По середине"]["Маленькая"],
                        'amount_on_middle_medium': fish_data["Предпочитаемая глубина"]["По середине"]["Средняя"],
                        'amount_on_middle_large': fish_data["Предпочитаемая глубина"]["По середине"]["Большая"],
                        'amount_on_top_small': fish_data["Предпочитаемая глубина"]["По верху"]["Маленькая"],
                        'amount_on_top_medium': fish_data["Предпочитаемая глубина"]["По верху"]["Средняя"],
                        'amount_on_top_large': fish_data["Предпочитаемая глубина"]["По верху"]["Большая"],
                        'filter': fish_data["filter"],
                        'rating': fish_data["rating"],
                        'bite_strength': fish_data["Сила поклёвки"],
                        'endurance_small': fish_data["Выносливость"]["Маленькая"],
                        'endurance_medium': fish_data["Выносливость"]["Средняя"],
                        'endurance_large': fish_data["Выносливость"]["Большая"],
                        'accuracy_small': fish_data["Аккуратность"]["Маленькая"],
                        'accuracy_medium': fish_data["Аккуратность"]["Средняя"],
                        'accuracy_large': fish_data["Аккуратность"]["Большая"],
                        'day_activity_small': fish_data["Активность днём"]["Маленькая"],
                        'day_activity_medium': fish_data["Активность днём"]["Средняя"],
                        'day_activity_large': fish_data["Активность днём"]["Большая"],
                        'night_activity_small': fish_data["Активность ночью"]["Маленькая"],
                        'night_activity_medium': fish_data["Активность ночью"]["Средняя"],
                        'night_activity_large': fish_data["Активность ночью"]["Большая"],
                        'price': fish_data["price"],
                        'rate': fish_data["rate"],
                        'valuable_weight': fish_data["Зачётный вес"],
                        'experience': fish_data["experience"],
                        'experience_rate': fish_data["exp rate"],
                        'biting_direction': ensure_list(fish_data["Поклёвка"]),
                        'chum_base': ensure_list(fish_data["Основа прикормки"]),
                        'chum_aromatizer': ensure_list(fish_data["Ароматизатор"]),
                        'lures_small': fish_data["Наживки"]["Маленькая"],
                        'lures_medium': fish_data["Наживки"]["Средняя"],
                        'lures_large': fish_data["Наживки"]["Большая"]
                    }
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

            self.stdout.write(self.style.SUCCESS(
                f'Success! Created: {created_count}, Updated: {updated_count}'
            ))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                'Error: fish_data_v3.json not found! Make sure the file is in the same directory as manage.py'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))