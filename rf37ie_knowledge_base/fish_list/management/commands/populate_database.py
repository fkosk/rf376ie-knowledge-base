import json
from fish_list.models import Fish

def ensure_list(value):
    if isinstance(value, list):
        return value
    else:
        return [value]

with open('fish_data_v3.json', 'r', encoding='utf-8') as f:
    fish_dict = json.load(f)
    for fish in fish_dict:
        fish_obj = Fish(
            id = fish_dict[fish]["Код рыбы"],
            name = fish_dict[fish]["Вид"]["Именительный"],
            min_weight = fish_dict[fish]["Минимальный вес"],
            max_weight = fish_dict[fish]["Максимальный вес"],
            min_depth_small = fish_dict[fish]["Минимальная глубина"]["Маленькая"],
            min_depth_medium = fish_dict[fish]["Минимальная глубина"]["Средняя"],
            min_depth_large = fish_dict[fish]["Минимальная глубина"]["Большая"],
            amount_on_bottom_small = fish_dict[fish]["Предпочитаемая глубина"]["По дну"]["Маленькая"],
            amount_on_bottom_medium = fish_dict[fish]["Предпочитаемая глубина"]["По дну"]["Средняя"],
            amount_on_bottom_large = fish_dict[fish]["Предпочитаемая глубина"]["По дну"]["Большая"],
            amount_on_middle_small = fish_dict[fish]["Предпочитаемая глубина"]["По середине"]["Маленькая"],
            amount_on_middle_medium = fish_dict[fish]["Предпочитаемая глубина"]["По середине"]["Средняя"],
            amount_on_middle_large = fish_dict[fish]["Предпочитаемая глубина"]["По середине"]["Большая"],
            amount_on_top_small = fish_dict[fish]["Предпочитаемая глубина"]["По верху"]["Маленькая"],
            amount_on_top_medium = fish_dict[fish]["Предпочитаемая глубина"]["По верху"]["Средняя"],
            amount_on_top_large = fish_dict[fish]["Предпочитаемая глубина"]["По верху"]["Большая"],
            filter = fish_dict[fish]["filter"],
            rating = fish_dict[fish]["rating"],
            bite_strength = fish_dict[fish]["Сила поклёвки"],
            endurance_small = fish_dict[fish]["Выносливость"]["Маленькая"],
            endurance_medium = fish_dict[fish]["Выносливость"]["Средняя"],
            endurance_large = fish_dict[fish]["Выносливость"]["Большая"],
            accuracy_small = fish_dict[fish]["Аккуратность"]["Маленькая"],
            accuracy_medium = fish_dict[fish]["Аккуратность"]["Средняя"],
            accuracy_large = fish_dict[fish]["Аккуратность"]["Большая"],
            day_activity_small = fish_dict[fish]["Активность днём"]["Маленькая"],
            day_activity_medium = fish_dict[fish]["Активность днём"]["Средняя"],
            day_activity_large = fish_dict[fish]["Активность днём"]["Большая"],
            night_activity_small = fish_dict[fish]["Активность ночью"]["Маленькая"],
            night_activity_medium = fish_dict[fish]["Активность ночью"]["Средняя"],
            night_activity_large = fish_dict[fish]["Активность ночью"]["Большая"],
            price = fish_dict[fish]["price"],
            rate = fish_dict[fish]["rate"],
            valuable_weight = fish_dict[fish]["Зачётный вес"],
            experience = fish_dict[fish]["experience"],
            experience_rate = fish_dict[fish]["exp rate"],
            biting_direction = ensure_list(fish_dict[fish]["Поклёвка"]),
            chum_base = ensure_list(fish_dict[fish]["Основа прикормки"]),
            chum_aromatizer = ensure_list(fish_dict[fish]["Ароматизатор"]),
            lures_small = fish_dict[fish]["Наживки"]["Маленькая"],
            lures_medium = fish_dict[fish]["Наживки"]["Средняя"],
            lures_large = fish_dict[fish]["Наживки"]["Большая"]
        )
        fish_obj.save()