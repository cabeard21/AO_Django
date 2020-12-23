from django.db import models


class EquipmentSet(models.Model):

    set_name = models.CharField(max_length=100, unique=True)
    items = models.ManyToManyField('ItemTier')
    target_ip = models.IntegerField(default=0)
    character = models.ForeignKey('Character', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.set_name

    def get_items(self):
        return [item.item.item_name for item in self.items.all()]

    def get_min_tiers(self):
        return [item.min_tier for item in self.items.all()]

    def get_mastery(self):
        res = []
        for item in self.items.all():
            res.append(self.character.get_spec(item.item.item_type.item_type))

        if len(res) == 0:
            res = [0*len(self.items)]

        return res


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

    def get_spec(self, item_type):
        for spec in self.mastery.all():
            if spec.item_type.item_type == item_type:
                return spec.spec_bonus

        return 0

        # return self.mastery.get(item_type__item_type=item_type).spec_bonus


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
