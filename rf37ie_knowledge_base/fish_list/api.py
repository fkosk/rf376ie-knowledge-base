import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Fish, FishLog, Bait, SpinningLure, Pref, Base

def get_field_verbose_names(request):
    """
    Get verbose names for all fields in the Fish model.
    Returns a dictionary mapping field names to their verbose names.
    """
    field_names = {}
    for field in Fish._meta.fields:
        # Use verbose_name if set, otherwise fall back to field name
        field_names[field.name] = field.verbose_name if field.verbose_name else field.name
    return field_names

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
        'field_names_ru': get_field_verbose_names(request)
    })

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

def get_filter_options(request):
    """API endpoint to get filter options based on current selections"""
    fish_name = request.GET.get('fish_name', '')
    base_name = request.GET.get('base_name', '')
    location_name = request.GET.get('location_name', '')

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


def find_average_bait_efficiency(request):
    """
    Calculate average bait efficiency across multiple fish.
    - Regular baits: use Fish efficiency directly
    - Spinning lures: multiply Fish efficiency by Pref efficiency per individual lure
    """
    fish_ids_str = request.GET.get('fish_ids', '')
    sizes_str = request.GET.get('sizes', '')
    base = request.GET.get('base', '')

    if not fish_ids_str:
        return JsonResponse({'Ошибка': 'Выберите ID хотя бы одной рыбы'}, status=400)

    fish_ids = [fid.strip() for fid in fish_ids_str.split(',') if fid.strip()]

    if sizes_str:
        sizes = [int(s.strip()) for s in sizes_str.split(',') if s.strip()]
    else:
        sizes = [3] * len(fish_ids)

    if len(sizes) != len(fish_ids):
        return JsonResponse({
            'Ошибка': f'Видов рыбы {len(fish_ids)}, а размеров - {len(sizes)}. Их количество должно совпадать'
        }, status=400)

    size_to_field = {
        1: 'lures_small',
        2: 'lures_medium',
        3: 'lures_large',
    }

    size_suffix = {
        1: 'Мал.',
        2: 'Сред.',
        3: 'Больш.',
    }

    fish_objects = Fish.objects.filter(id__in=fish_ids)
    fish_map = {fish.id: fish for fish in fish_objects}

    # Preload Pref data if base specified
    pref_data = {}
    if base:
        prefs = Pref.objects.filter(base__iexact=base, fish_id__in=fish_ids)
        for pref in prefs:
            pref_data[pref.fish_id] = pref.spinning_lures

    # Preload Bait translations
    bait_translations = {}
    for bait in Bait.objects.all():
        bait_translations[bait.dev_name] = bait.russian_name

    total_fish = len(fish_ids)
    bait_totals = {}
    bait_fish_count = {}

    for fish_id, size in zip(fish_ids, sizes):
        fish = fish_map.get(fish_id)
        if not fish:
            continue

        field_name = size_to_field.get(size)
        if not field_name:
            continue

        lures = getattr(fish, field_name, {})
        if not lures:
            continue

        for bait_name, fish_efficiency in lures.items():
            # Check if spinning lure (has _1, _2, _3 suffix)
            if '_' in bait_name:
                parts = bait_name.rsplit('_', 1)
                if parts[-1] in ('1', '2', '3'):
                    lure_type = parts[0]
                    size_code = parts[-1]
                    size_label = size_suffix.get(int(size_code), '')

                    # Only break down into individual lures if base is selected
                    if base and fish_id in pref_data:
                        individual_lures = SpinningLure.objects.filter(lure_type=lure_type)
                        fish_prefs = pref_data[fish_id]

                        for spinner in individual_lures:
                            pref_efficiency = fish_prefs.get(spinner.lure_name, 0)
                            if pref_efficiency > 0:
                                final_score = fish_efficiency * pref_efficiency / 100
                                result_key = f"{spinner.lure_name} ({size_label})"

                                if result_key not in bait_totals:
                                    bait_totals[result_key] = 0
                                    bait_fish_count[result_key] = 0

                                bait_totals[result_key] += final_score
                                bait_fish_count[result_key] += 1
                    else:
                        # No base - treat spinner type as regular bait
                        if bait_name not in bait_totals:
                            bait_totals[bait_name] = 0
                            bait_fish_count[bait_name] = 0
                        bait_totals[bait_name] += fish_efficiency
                        bait_fish_count[bait_name] += 1

                    continue

            # Regular bio bait
            if bait_name not in bait_totals:
                bait_totals[bait_name] = 0
                bait_fish_count[bait_name] = 0

            bait_totals[bait_name] += fish_efficiency
            bait_fish_count[bait_name] += 1

    # Calculate average
    bait_spread = []
    for bait_name in bait_totals:
        if bait_fish_count[bait_name] > 0:
            avg_score = bait_totals[bait_name] / total_fish
            bait_spread.append({
                'bait_name': bait_name,
                'average_score': round(avg_score, 2),
                'total_score': round(bait_totals[bait_name], 2),
                'fish_count': bait_fish_count[bait_name],
                'total_fish': total_fish,
            })

    bait_spread.sort(key=lambda x: x['average_score'], reverse=True)

    # Add Russian names
    for bait in bait_spread:
        # Check if it's an individual lure with size suffix
        name = bait['bait_name']
        if ' (' in name:
            # "Circl-5000 (Мал.)" -> just use as display name
            bait['russian_name'] = name
            bait['lure_type'] = None
        else:
            # Regular bait - look up translation
            bait['russian_name'] = bait_translations.get(name, name)
            bait['lure_type'] = None

    return JsonResponse({'bait_spread': bait_spread})

def get_fish_list(request):
    """API endpoint to return all fish names with their variants (regular, trophy, albino)"""
    fish_list = []

    for fish in Fish.objects.all():
        fish_id = fish.id

        # Determine variant
        if 'installsoft' in fish_id.lower():
            variant = 'Трофей'
        elif 'A' in fish_id or 'А' in fish_id:  # Latin A or Cyrillic А
            variant = 'Альбинос'
        else:
            variant = 'Обычный'

        fish_list.append({
            'id': fish.id,
            'name': fish.name,
            'display_name': f"{fish.name} - {variant}" if variant != 'Обычный' else fish.name,
            'variant': variant,
        })

    # Sort by name then variant
    fish_list.sort(key=lambda x: (x['name'], x['variant']))

    return JsonResponse({'fish_list': fish_list})

def get_bases(request):
    """API endpoint to return all bases"""
    bases = list(Base.objects.values('dev_name', 'russian_name').order_by('russian_name'))
    return JsonResponse({'bases': bases})