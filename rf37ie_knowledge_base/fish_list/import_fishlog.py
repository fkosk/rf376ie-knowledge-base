from .models import FishLog

def import_fish_log(filepath):
    with open(filepath, 'r') as file:
        for line in file:
            split_line = line.strip().split(":")
            fish_log = FishLog(
                fish_name = split_line[0],
                fish_weight = split_line[1],
                bait_name = split_line[2],
                base_name = split_line[3],
                location_name = split_line[4],
                fish_id = split_line[5],
                time = split_line[6],
                depth = split_line[7]
            )
            fish_log.save()