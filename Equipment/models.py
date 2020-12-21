from django.db import models


class EquipmentSet(models.Model):

    set_name = models.CharField(max_length=100, unique=True)
    items = models.ManyToManyField('ItemTier')    

    def __str__(self):
        return self.set_name


class ItemTier(models.Model):
    item = models.ForeignKey('Item', on_delete=models.DO_NOTHING, related_name='itemtier_item')
    min_tier = models.IntegerField(default=4, verbose_name='Minimum Tier')

    def __str__(self):
        return f"{self.item} > {self.min_tier}"


class Item(models.Model):

    class QualityEnum(models.IntegerChoices):
        NORMAL = 1,
        GOOD = 2,
        OUTSTANDING = 3,
        EXCELLENT = 4,
        MASTERPIECE = 5,

    item_name = models.CharField(max_length=50)
    tier = models.IntegerField(default=4)
    quality = models.IntegerField(default=QualityEnum.NORMAL, choices=QualityEnum.choices)
