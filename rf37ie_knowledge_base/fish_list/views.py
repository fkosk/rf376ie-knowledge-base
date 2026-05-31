from django.shortcuts import render
from django.http import JsonResponse
from .models import Fish
import json
import os

FIELD_NAMES_RU = {
    'id': 'ID Рыбы',
    'name': 'Название рыбы',
    'min_weight': 'Мин. вес',
    'max_weight': 'Макс. вес',
    'min_depth_small': 'Мин. глубина (мал.)',
    'min_depth_medium': 'Мин. глубина (сред.)',
    'min_depth_large': 'Мин. глубина (круп.)',
    'amount_on_bottom_small': 'Кол-во на дне (мал.)',
    'amount_on_bottom_medium': 'Кол-во на дне (сред.)',
    'amount_on_bottom_large': 'Кол-во на дне (круп.)',
    'amount_on_middle_small': 'Кол-во в толще (мал.)',
    'amount_on_middle_medium': 'Кол-во в толще (сред.)',
    'amount_on_middle_large': 'Кол-во в толще (круп.)',
    'amount_on_top_small': 'Кол-во у поверхности (мал.)',
    'amount_on_top_medium': 'Кол-во у поверхности (сред.)',
    'amount_on_top_large': 'Кол-во у поверхности (круп.)',
    'filter': 'Фильтр',
    'rating': 'Рейтинг',
    'bite_strength': 'Сила поклевки',
    'endurance_small': 'Выносливость (мал.)',
    'endurance_medium': 'Выносливость (сред.)',
    'endurance_large': 'Выносливость (круп.)',
    'accuracy_small': 'Аккуратность (мал.)',
    'accuracy_medium': 'Аккуратность (сред.)',
    'accuracy_large': 'Аккуратность (круп.)',
    'day_activity_small': 'Дневная активность (мал.)',
    'day_activity_medium': 'Дневная активность (сред.)',
    'day_activity_large': 'Дневная активность (круп.)',
    'night_activity_small': 'Ночная активность (мал.)',
    'night_activity_medium': 'Ночная активность (сред.)',
    'night_activity_large': 'Ночная активность (круп.)',
    'price': 'Цена',
    'rate': 'Курс',
    'valuable_weight': 'Зачётный вес',
    'experience': 'Опыт',
    'experience_rate': 'Коэффициент опыта',
    'biting_direction': 'Направление поклевки',
    'chum_base': 'Основа прикормки',
    'chum_aromatizer': 'Ароматизатор прикормки',
    'lures_small': 'Наживки (мал.)',
    'lures_medium': 'Наживки (сред.)',
    'lures_large': 'Наживки (круп.)',
}


def get_fish_image_url(fish_id):
    """
    Find the correct image for a fish.
    First checks for regular fish image, then for installsoft (trophy) image.
    """
    static_dir = os.path.join('fish_list', 'static', 'fish_list', 'fish_pics')

    # Possible image names in order of preference
    possible_names = [
        f"{fish_id}.png",
        f"{fish_id}installsoft.png",
    ]

    for image_name in possible_names:
        image_path = os.path.join(static_dir, image_name)
        if os.path.exists(image_path):
            return f"/static/fish_list/fish_pics/{image_name}"

    return None


def fish_list(request):
    """Main view displaying all fish in a table"""
    fish = Fish.objects.all()
    fields = [field.name for field in Fish._meta.fields]

    context = {
        'fish': fish,
        'fields': fields,
        'field_names_ru': FIELD_NAMES_RU,
    }
    return render(request, 'fish_list/fish_list.html', context)


def fish_search(request):
    """Search view for finding specific fish"""
    fish = None
    error_message = None
    fish_image_url = None
    is_trophy = False

    if request.method == 'GET' and ('name' in request.GET or 'id' in request.GET):
        fish_name = request.GET.get('name', '').strip()
        fish_id = request.GET.get('id', '').strip()

        if fish_name or fish_id:
            try:
                if fish_id:
                    fish = Fish.objects.get(id=fish_id)
                elif fish_name:
                    fish = Fish.objects.get(name__iexact=fish_name)

                if fish:
                    # Get the correct image URL
                    fish_image_url = get_fish_image_url(fish.id)

                    # Check if it's a trophy (installsoft) image
                    if fish_image_url and 'installsoft' in fish_image_url:
                        is_trophy = True

            except Fish.DoesNotExist:
                error_message = "Рыба не найдена"
            except Fish.MultipleObjectsReturned:
                if fish_id:
                    fish = Fish.objects.filter(id=fish_id).first()
                elif fish_name:
                    fish = Fish.objects.filter(name__iexact=fish_name).first()

                if fish:
                    fish_image_url = get_fish_image_url(fish.id)
                    if fish_image_url and 'installsoft' in fish_image_url:
                        is_trophy = True

    context = {
        'fish': fish,
        'error_message': error_message,
        'field_names_ru': FIELD_NAMES_RU,
        'fish_image_url': fish_image_url,
        'is_trophy': is_trophy,
        'search_name': request.GET.get('name', ''),
        'search_id': request.GET.get('id', ''),
    }

    return render(request, 'fish_list/fish_search.html', context)


def get_fish_data(request):
    """API endpoint to return fish data as JSON"""
    fish = Fish.objects.all()
    fish_data = []

    for f in fish:
        fish_dict = {}
        for field in Fish._meta.fields:
            value = getattr(f, field.name)
            if isinstance(value, list):
                value = ', '.join(str(v) for v in value)
            elif isinstance(value, dict):
                value = json.dumps(value, ensure_ascii=False)
            fish_dict[field.name] = value
        fish_data.append(fish_dict)

    return JsonResponse({
        'fish_data': fish_data,
        'field_names_ru': FIELD_NAMES_RU
    })