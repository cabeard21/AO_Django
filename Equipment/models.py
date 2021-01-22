from django.db import models
from django.db.models import F


class EquipmentSet(models.Model):

    set_name = models.CharField(max_length=100, unique=True)
    items = models.ManyToManyField('ItemTier')
    character = models.ForeignKey('Character', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.set_name

    def get_items(self):
        return [item.item.item_name for item in self.items.all()]

    def get_min_tiers(self):
        return [item.min_tier for item in self.items.all()]

    def get_target_ips(self):
        return [item.target_ip for item in self.items.all()]

    def get_mastery(self):
        if self.character is None:
            return [0 for i in range(len(self.items.all()))]

        res = []
        for item in self.items.all():
            res.append(self.character.get_spec(item.item.item_name))

        return res


class ItemTier(models.Model):
    item = models.ForeignKey('Item', on_delete=models.DO_NOTHING, related_name='itemtier_item')
    min_tier = models.IntegerField(default=4, verbose_name='Minimum Tier')
    target_ip = models.IntegerField(
        default=0,
        verbose_name='Target IP',
        help_text='Positive for cheapest, negative for highest IP/Cost'
    )

    def __str__(self):
        return f"{self.item} > {self.min_tier} > {self.target_ip}"

    class Meta:
        ordering = [F("item__item_name")]


# Fixture
class Item(models.Model):

    item_name = models.CharField(max_length=50)
    item_type = models.ForeignKey('ItemType', on_delete=models.DO_NOTHING, related_name='item_itemtype')

    def __str__(self):
        return self.item_name


class Character(models.Model):

    char_name = models.CharField(max_length=100, unique=True)
    mastery = models.ManyToManyField('ItemSpec')

    def __str__(self):
        return self.char_name

    def get_spec(self, item_name):
        for spec in self.mastery.all():
            if spec.item.item_name == item_name:
                return spec.spec_bonus

        return 0

        # return self.mastery.get(item_type__item_type=item_type).spec_bonus


class ItemSpec(models.Model):

    item = models.ForeignKey('Item', on_delete=models.DO_NOTHING, related_name='itemspec_item')
    spec_bonus = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.item}: {self.spec_bonus}"

    class Meta:
        ordering = [F("item__item_name")]


# Fixture
class ItemType(models.Model):

    item_type = models.CharField(max_length=50)

    def __str__(self):
        return self.item_type
