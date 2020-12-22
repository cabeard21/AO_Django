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


# Fixture
class Item(models.Model):

    item_name = models.CharField(max_length=50)
    tier = models.IntegerField(default=4)
    item_type = models.ForeignKey('ItemType', on_delete=models.DO_NOTHING, related_name='item_itemtype')

    def __str__(self):
        return self.item_name


class Character(models.Model):

    char_name = models.CharField(max_length=100, unique=True)
    mastery = models.ManyToManyField('ItemTypeSpec')

    def __str__(self):
        return self.char_name


class ItemTypeSpec(models.Model):

    item_type = models.ForeignKey('ItemType', on_delete=models.DO_NOTHING, related_name='itemtypespec_itemtype')
    spec_bonus = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.item_type}: {self.spec_bonus}"


# Fixture
class ItemType(models.Model):

    item_type = models.CharField(max_length=50)

    def __str__(self):
        return self.item_type
