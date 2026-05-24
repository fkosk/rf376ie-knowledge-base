import json
from fish_list.models import Fish

with open('fish_list.json', 'r') as f:
    fish_dict = json.load(f)
    for fish in fish_dict:
        fish_obj = Fish(
            id = fish["Код рыбы"],
            name = fish["Вид"]["Именительный"],
            min_weight = fish["Минимальный вес"],
            max_weight = fish["Максимальный вес"],
            min_depth_small = fish["Минимальная глубина"]["Маленькая"],
            min_depth_medium = fish["Минимальная глубина"]["Средняя"],
            min_depth_large = fish["Минимальная глубина"]["Большая"],
            amount_on_bottom_small = fish["Предпочитаемая глубина"]["По дну"]["Маленькая"],
            amount_on_bottom_medium = fish["Предпочитаемая глубина"]["По дну"]["Средняя"],
            amount_on_bottom_large = fish["Предпочитаемая глубина"]["По дну"]["Большая"],
            amount_on_middle_small = fish["Предпочитаемая глубина"]["По середине"]["Маленькая"],
            amount_on_middle_medium = fish["Предпочитаемая глубина"]["По середине"]["Средняя"],
            amount_on_middle_large = fish["Предпочитаемая глубина"]["По середине"]["Большая"],
            amount_on_top_small = fish["Предпочитаемая глубина"]["По верху"]["Маленькая"],
            amount_on_top_medium = fish["Предпочитаемая глубина"]["По верху"]["Средняя"],
            amount_on_top_large = fish["Предпочитаемая глубина"]["По верху"]["Большая"],
            filter = fish["filter"],
            rating = fish["rating"],
            bite_strength = fish["Сила поклёвки"],
            endurance_small = fish["Выносливость"]["Маленькая"],
            endurance_medium = fish["Выносливость"]["Средняя"],
            endurance_large = fish["Выносливость"]["Большая"],
            accuracy_small = fish["Аккуратность"]["Маленькая"],
            accuracy_medium = fish["Аккуратность"]["Средняя"],
            accuracy_large = fish["Аккуратность"]["Большая"],
            day_activity_small = fish["Активность днём"]["Маленькая"],
            day_activity_medium = fish["Активность днём"]["Средняя"],
            day_activity_large = fish["Активность днём"]["Большая"],
            night_activity_small = fish["Активность ночью"]["Маленькая"],
            night_activity_medium = fish["Активность ночью"]["Средняя"],
            night_activity_large = fish["Активность ночью"]["Большая"],
            price = fish["price"],
            rate = fish["rate"],
            valuable_weight = fish["Зачётный вес"],
            experience = fish["experience"],
            experience_rate = fish["exp rate"],
            biting_direction = fish["Поклёвка"],
            chum_base = fish["Основа прикормки"],
            chum_aromatizer = fish["Ароматизатор"],
            lures_small = fish["Наживки"]["Маленькая"],
            lures_medium = fish["Наживки"]["Средняя"],
            lures_large = fish["Наживки"]["Большая"]
        )
        fish_obj.save()