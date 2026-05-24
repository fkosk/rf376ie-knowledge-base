from django.db import models

# Create your models here.
class Fish(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    min_weight = models.IntegerField()
    max_weight = models.IntegerField()

    min_depth_small = models.IntegerField()
    min_depth_medium = models.IntegerField()
    min_depth_large = models.IntegerField()

    amount_on_bottom_small = models.IntegerField()
    amount_on_bottom_medium = models.IntegerField()
    amount_on_bottom_large = models.IntegerField()

    amount_on_middle_small = models.IntegerField()
    amount_on_middle_medium = models.IntegerField()
    amount_on_middle_large = models.IntegerField()

    amount_on_top_small = models.IntegerField()
    amount_on_top_medium = models.IntegerField()
    amount_on_top_large = models.IntegerField()

    filter = models.IntegerField()
    rating = models.IntegerField()
    bite_strength = models.IntegerField()

    endurance_small = models.IntegerField()
    endurance_medium = models.IntegerField()
    endurance_large = models.IntegerField()

    accuracy_small = models.IntegerField()
    accuracy_medium = models.IntegerField()
    accuracy_large = models.IntegerField()

    day_activity_small = models.IntegerField()
    day_activity_medium = models.IntegerField()
    day_activity_large = models.IntegerField()

    night_activity_small = models.IntegerField()
    night_activity_medium = models.IntegerField()
    night_activity_large = models.IntegerField()

    price = models.IntegerField()
    rate = models.IntegerField()
    valuable_weight = models.IntegerField()
    experience = models.IntegerField()
    experience_rate = models.IntegerField()
    biting_direction = models.CharField(max_length=20)
    chum_base = models.CharField(max_length=20)
    chum_aromatizer = models.CharField(max_length=20)

    lures_small = models.JSONField()
    lures_medium = models.JSONField()
    lures_large = models.JSONField()

    def __str__(self):
        return self.name