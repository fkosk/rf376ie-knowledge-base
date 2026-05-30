from django.db import models

from rf37ie_knowledge_base.fish_list.models import Fish

# Create your models here.
class FishLog(models.Model):
    fish_name = models.ForeignKey(Fish, to_field='name', on_delete=models.CASCADE)
    fish_weight = models.IntegerField()
    bait_name = models.CharField(max_length=255)
    base_name = models.CharField(max_length=255)
    location_name = models.CharField(max_length=255)
    fish_id = models.ForeignKey(Fish, to_field='id', on_delete=models.CASCADE)
    time = models.CharField(max_length=255)
    depth = models.IntegerField()

