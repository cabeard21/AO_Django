from django.db import models
from django.db.models import F

class BootSpeed(models.Model):

    boot = models.ForeignKey('Boot', on_delete=models.DO_NOTHING, related_name='bootspeed_boot')
    speed = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.boot}"

    class Meta:
        ordering = [F("boot__boot_name")]

class MountSpeedWeight(models.Model):

    mount = models.ForeignKey('Mount', on_delete=models.DO_NOTHING, related_name='mountspeedweight_mount')
    tier = models.IntegerField(default=3)
    speed = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.mount} (T{self.tier})"

    class Meta:
        ordering = [F("mount__mount_name")]

class BagWeight(models.Model):

    bag = models.ForeignKey('Bag', on_delete=models.DO_NOTHING, related_name='bagweight_bag')
    tier = models.IntegerField(default=3)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.bag} (T{self.tier})"

    class Meta:
        ordering = [F("bag__bag_name")]

# Fixture
class Boot(models.Model):

    boot_name = models.CharField(max_length=50)

    def __str__(self):
        return self.boot_name

class Mount(models.Model):

    mount_name = models.CharField(max_length=50)

    def __str__(self):
        return self.mount_name

class Bag(models.Model):

    bag_name = models.CharField(max_length=50)

    def __str__(self):
        return self.bag_name
