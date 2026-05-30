from rf37ie_knowledge_base.fishlog_importer.models import FishLog
from collections import defaultdict

def generate_fish_list_per_base():
    pairs = FishLog.objects.values_list('base_name', 'fish_name__name').distinct()

    base_data = defaultdict(set)
    for base_name, fish_name in pairs:
        base_data[base_name].add(fish_name)

    return dict(base_data)