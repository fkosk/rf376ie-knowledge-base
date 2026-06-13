from django.shortcuts import render
from django.http import JsonResponse
from .models import Fish, FishLog
import json
import os
from .import_fishlog import import_fish_log

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


def get_field_verbose_names():
    """
    Get verbose names for all fields in the Fish model.
    Returns a dictionary mapping field names to their verbose names.
    """
    field_names = {}
    for field in Fish._meta.fields:
        # Use verbose_name if set, otherwise fall back to field name
        field_names[field.name] = field.verbose_name if field.verbose_name else field.name
    return field_names


def fish_list(request):
    """Main view displaying all fish in a table"""
    fish = Fish.objects.all()
    fields = [field.name for field in Fish._meta.fields]
    field_names_ru = get_field_verbose_names()

    context = {
        'fish': fish,
        'fields': fields,
        'field_names_ru': field_names_ru,
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

    field_names_ru = get_field_verbose_names()

    context = {
        'fish': fish,
        'error_message': error_message,
        'field_names_ru': field_names_ru,
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
        'field_names_ru': get_field_verbose_names()
    })

def import_fishlog(request):
    success_message = None
    error_message = None

    if request.method == 'POST':
        filepath = request.POST.get('filepath')

        if filepath:
            try:
                import_fish_log(filepath)
                success_message = "Файл успешно импортирован!"
            except FileNotFoundError:
                error_message = "Файл не найден. Проверьте путь."
            except Exception as e:
                error_message = f"Ошибка: {str(e)}"
        else:
            error_message = "Пожалуйста, укажите путь к файлу"

    context = {
        'success_message': success_message,
        'error_message': error_message,
    }

    return render(request, 'fish_list/fishlog_importer.html', context)