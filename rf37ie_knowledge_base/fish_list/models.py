from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Fish(models.Model):
    id = models.CharField(primary_key=True, verbose_name='ID рыбы')
    name = models.CharField(max_length=255, verbose_name='Название вида')

    min_weight = models.IntegerField(verbose_name='Мин. вес')
    max_weight = models.IntegerField(verbose_name='Макс. вес')

    min_depth_small = models.IntegerField(verbose_name='Мин. глубина (мал.)')
    min_depth_medium = models.IntegerField(verbose_name='Мин. глубина (сред.)')
    min_depth_large = models.IntegerField(verbose_name='Мин. глубина (круп.)')

    amount_on_bottom_small = models.IntegerField(verbose_name='Кол-во на дне (мал.)')
    amount_on_bottom_medium = models.IntegerField(verbose_name='Кол-во на дне (сред.)')
    amount_on_bottom_large = models.IntegerField(verbose_name='Кол-во на дне (круп.)')

    amount_on_middle_small = models.IntegerField(verbose_name='Кол-во в толще (мал.)')
    amount_on_middle_medium = models.IntegerField(verbose_name='Кол-во в толще (сред.)')
    amount_on_middle_large = models.IntegerField(verbose_name='Кол-во в толще (круп.)')

    amount_on_top_small = models.IntegerField(verbose_name='Кол-во у поверхности (мал.)')
    amount_on_top_medium = models.IntegerField(verbose_name='Кол-во у поверхности (сред.)')
    amount_on_top_large = models.IntegerField(verbose_name='Кол-во у поверхности (круп.)')

    filter = models.IntegerField(verbose_name='Фильтр')
    rating = models.IntegerField(verbose_name='Рейтинг')
    bite_strength = models.IntegerField(verbose_name='Сила поклевки')

    endurance_small = models.IntegerField(verbose_name='Выносливость (мал.)')
    endurance_medium = models.IntegerField(verbose_name='Выносливость (сред.)')
    endurance_large = models.IntegerField(verbose_name='Выносливость (круп.)')

    accuracy_small = models.IntegerField(verbose_name='Аккуратность (мал.)')
    accuracy_medium = models.IntegerField(verbose_name='Аккуратность (сред.)')
    accuracy_large = models.IntegerField(verbose_name='Аккуратность (круп.)')

    day_activity_small = models.IntegerField(verbose_name='Дневная активность (мал.)')
    day_activity_medium = models.IntegerField(verbose_name='Дневная активность (сред.)')
    day_activity_large = models.IntegerField(verbose_name='Дневная активность (круп.)')

    night_activity_small = models.IntegerField(verbose_name='Ночная активность (мал.)')
    night_activity_medium = models.IntegerField(verbose_name='Ночная активность (сред.)')
    night_activity_large = models.IntegerField(verbose_name='Ночная активность (круп.)')

    price = models.IntegerField(verbose_name='Цена')
    rate = models.IntegerField(verbose_name='Курс')
    valuable_weight = models.IntegerField(verbose_name='Зачётный вес')
    experience = models.IntegerField(verbose_name='Опыт')
    experience_rate = models.IntegerField(verbose_name='Коэффициент опыта')
    biting_direction = ArrayField(models.CharField(max_length=20), blank=True, default=list, verbose_name='Направление поклевки')
    chum_base = ArrayField(models.CharField(max_length=20), blank=True, default=list, verbose_name='Основа прикормки')
    chum_aromatizer = ArrayField(models.CharField(max_length=20), blank=True, default=list, verbose_name='Ароматизатор прикормки')

    lures_small = models.JSONField(verbose_name='Наживки (мал.)')
    lures_medium = models.JSONField(verbose_name='Наживки (сред.)')
    lures_large = models.JSONField(verbose_name='Наживки (круп.)')

    def __str__(self):
        return self.name

class FishLog(models.Model):
    fish_name = models.CharField(max_length=255)
    fish_weight = models.IntegerField()
    bait_name = models.CharField(max_length=255)
    base_name = models.CharField(max_length=255)
    location_name = models.CharField(max_length=255)
    fish_id = models.ForeignKey(Fish, to_field='id', on_delete=models.CASCADE)
    time = models.CharField(max_length=255)
    depth = models.IntegerField()