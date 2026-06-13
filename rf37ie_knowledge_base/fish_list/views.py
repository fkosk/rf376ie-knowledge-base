from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
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


def get_all_fishlogs(request):
    """API endpoint to return paginated, sorted, filtered fishlogs as JSON"""
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 1000))
    sort_field = request.GET.get('sort', 'id')
    sort_order = request.GET.get('order', 'desc')

    # Dropdown filters
    fish_name = request.GET.get('fish_name', '')
    base_name = request.GET.get('base_name', '')
    location_name = request.GET.get('location_name', '')

    fishlogs = FishLog.objects.all()

    # Apply dropdown filters
    if fish_name:
        fishlogs = fishlogs.filter(fish_name=fish_name)
    if base_name:
        fishlogs = fishlogs.filter(base_name=base_name)
    if location_name:
        fishlogs = fishlogs.filter(location_name=location_name)

    # Validate sort field
    valid_sort_fields = [field.name for field in FishLog._meta.fields]
    if sort_field not in valid_sort_fields:
        sort_field = 'id'

    # Apply sorting
    if sort_order == 'asc':
        order_by = sort_field
    else:
        order_by = f'-{sort_field}'

    fishlogs = fishlogs.order_by(order_by)

    # Paginate
    paginator = Paginator(fishlogs, per_page)
    page_obj = paginator.get_page(page)

    # Preload all relevant fish data into a dictionary for fast lookup
    fish_ids = set(log.fish_id for log in page_obj)
    fish_data = {}
    for fish in Fish.objects.filter(id__in=fish_ids):
        is_trophy = 'installsoft' in fish.id.lower()
        fish_data[fish.id] = {
            'valuable_weight': fish.valuable_weight,
            'is_trophy': is_trophy,
        }

    fishlog_data = []
    for f in page_obj:
        fishlog_dict = {}
        for field in FishLog._meta.fields:
            value = getattr(f, field.name)
            if isinstance(value, list):
                value = ', '.join(str(v) for v in value)
            elif isinstance(value, dict):
                value = json.dumps(value, ensure_ascii=False)
            fishlog_dict[field.name] = value

        # Add fish info for styling
        fish_info = fish_data.get(f.fish_id)
        if fish_info:
            fishlog_dict['valuable_weight'] = fish_info['valuable_weight']
            fishlog_dict['is_trophy'] = fish_info['is_trophy']
        else:
            fishlog_dict['valuable_weight'] = 0
            fishlog_dict['is_trophy'] = False

        fishlog_data.append(fishlog_dict)

    return JsonResponse({
        'fishlog_data': fishlog_data,
        'total_pages': paginator.num_pages,
        'current_page': page,
        'total_records': paginator.count,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'sort_field': sort_field,
        'sort_order': sort_order,
    })

def fishlog_data(request):
    """View to display all fishlogs in a table"""
    return render(request, 'fish_list/fishlog_data.html')


def get_filter_options(request):
    """API endpoint to get filter options based on current selections"""
    fish_name = request.GET.get('fish_name', '')
    base_name = request.GET.get('base_name', '')
    location_name = request.GET.get('location_name', '')

    from django.db.models import Q

    # Base queryset
    queryset = FishLog.objects.all()

    # Apply current filters to get relevant options
    if fish_name:
        queryset = queryset.filter(fish_name=fish_name)
    if base_name:
        queryset = queryset.filter(base_name=base_name)
    if location_name:
        queryset = queryset.filter(location_name=location_name)

    # Get unique values for each field
    data = {
        'fish_names': list(queryset.values_list('fish_name', flat=True).distinct().order_by('fish_name')),
        'base_names': list(queryset.values_list('base_name', flat=True).distinct().order_by('base_name')),
        'location_names': list(queryset.values_list('location_name', flat=True).distinct().order_by('location_name')),
    }

    return JsonResponse(data)


def get_all_options(request):
    """API endpoint to get ALL possible filter options (for initial load)"""
    data = {
        'all_fish_names': list(FishLog.objects.values_list('fish_name', flat=True).distinct().order_by('fish_name')),
        'all_base_names': list(FishLog.objects.values_list('base_name', flat=True).distinct().order_by('base_name')),
        'all_location_names': list(
            FishLog.objects.values_list('location_name', flat=True).distinct().order_by('location_name')),
    }

    return JsonResponse(data)

def get_bait_statistics(request):
    """API endpoint to return bait statistics"""
    fish_name = request.GET.get('fish_name', '')
    base_name = request.GET.get('base_name', '')
    location_name = request.GET.get('location_name', '')

    if not fish_name:
        return JsonResponse({'statistics': []})

    queryset = FishLog.objects.filter(fish_name=fish_name)
    if base_name:
        queryset = queryset.filter(base_name=base_name)
    if location_name:
        queryset = queryset.filter(location_name=location_name)

    fish_data = {}
    for fish in Fish.objects.all():
        fish_data[fish.id] = {
            'valuable_weight': fish.valuable_weight,
            'is_trophy': 'installsoft' in fish.id.lower(),
        }

    all_logs = queryset.values_list('bait_name', 'fish_id', 'fish_weight')

    bait_stats = {}
    bait_order = []

    for bait_name, fish_id, weight in all_logs:
        if bait_name not in bait_stats:
            bait_stats[bait_name] = {'total': 0, 'regular': 0, 'valuable': 0, 'trophies': 0}
            bait_order.append(bait_name)

        bait_stats[bait_name]['total'] += 1

        fish_info = fish_data.get(fish_id)
        if fish_info:
            if fish_info['is_trophy']:
                bait_stats[bait_name]['trophies'] += 1
            elif weight > fish_info['valuable_weight']:
                bait_stats[bait_name]['valuable'] += 1
            else:
                bait_stats[bait_name]['regular'] += 1
        else:
            bait_stats[bait_name]['regular'] += 1

    statistics = []
    for bait in bait_order:
        stats = bait_stats[bait]
        statistics.append({
            'bait_name': bait,
            'total': stats['total'],
            'regular': stats['regular'],
            'valuable': stats['valuable'],
            'trophies': stats['trophies'],
        })

    return JsonResponse({'statistics': statistics})