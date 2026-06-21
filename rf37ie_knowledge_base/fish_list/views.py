from django.shortcuts import render
from .models import Fish, FishLog
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

def fish_list(request):
    """Main view displaying all fish in a table"""
    fish = Fish.objects.all().values()
    fields = [field.name for field in Fish._meta.fields]

    fish_data = []
    for f in fish:
        processed = {}
        for field_name, value in f.items():
            if isinstance(value, list):
                processed[field_name] = ', '.join(str(v) for v in value)
            elif isinstance(value, dict):
                parts = [f"{k}: {v}" for k, v in value.items()]
                processed[field_name] = ', '.join(parts)
            else:
                processed[field_name] = value if value is not None else ''
        fish_data.append(processed)

    context = {
        'fish_data': fish_data,
        'fields': fields,
        'field_names_ru': {field.name: field.verbose_name for field in Fish._meta.fields},
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
        'fish_image_url': fish_image_url,
        'is_trophy': is_trophy,
        'search_name': request.GET.get('name', ''),
        'search_id': request.GET.get('id', ''),
    }

    return render(request, 'fish_list/fish_search.html', context)

def import_fishlog(request):
    """Fishlog importer view"""
    success_message = None
    error_message = None
    created = 0
    skipped = 0

    if request.method == 'POST':
        filepath = request.POST.get('filepath')

        if filepath:
            try:
                created, skipped = import_fish_log(filepath)
                success_message = f"✅ Создано: {created}, ⏭️ Пропущено: {skipped}"
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

def fishlog_data(request):
    """View to display all fishlogs in a table"""
    return render(request, 'fish_list/fishlog_data.html')