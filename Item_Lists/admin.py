from django.contrib import admin

from .models import *

@admin.register(BootSpeed)
class BootSpeedAdmin(admin.ModelAdmin):
    autocomplete_fields = ['boot']

@admin.register(MountSpeedWeight)
class MountSpeedWeightAdmin(admin.ModelAdmin):
    autocomplete_fields = ['mount']

@admin.register(BagWeight)
class BagWeightAdmin(admin.ModelAdmin):
    autocomplete_fields = ['bag']

@admin.register(Boot)
class BootAdmin(admin.ModelAdmin):
    ordering = ['boot_name']
    search_fields = ['boot_name']

@admin.register(Mount)
class MountAdmin(admin.ModelAdmin):
    ordering = ['mount_name']
    search_fields = ['mount_name']

@admin.register(Bag)
class BagAdmin(admin.ModelAdmin):
    ordering = ['bag_name']
    search_fields = ['bag_name']
