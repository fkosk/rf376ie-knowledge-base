from .models import Fish, FishLog
from django.db import transaction

def import_fish_log(filepath):
    created_count = 0
    skipped_count = 0

    print("Loading fish IDs...")
    valid_fish_ids = set(Fish.objects.values_list('id', flat=True))
    print(f"Loaded {len(valid_fish_ids)} fish IDs")

    batch = []
    batch_size = 10000

    with open(filepath, 'r') as file:
        for line_num, line in enumerate(file, 1):
            try:
                split_line = line.strip().split(":")

                fish_id = split_line[5]

                if fish_id not in valid_fish_ids:
                    skipped_count += 1
                    continue

                batch.append(FishLog(
                    fish_name=split_line[0],
                    fish_weight=split_line[1],
                    bait_name=split_line[2],
                    base_name=split_line[3],
                    location_name=split_line[4],
                    fish_id=fish_id,
                    time=split_line[6],
                    depth=split_line[7]
                ))

                if len(batch) >= batch_size:
                    with transaction.atomic():
                        FishLog.objects.bulk_create(batch)
                    created_count += len(batch)
                    batch = []

                    if created_count % 100000 == 0:
                        print(f"Imported {created_count} records...")

            except (IndexError, ValueError) as e:
                skipped_count += 1
                continue

    if batch:
        with transaction.atomic():
            FishLog.objects.bulk_create(batch)
        created_count += len(batch)

    print(f"Done! Created: {created_count}, Skipped: {skipped_count}")
    return created_count, skipped_count