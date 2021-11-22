from django.contrib import admin

from .models import *


@admin.register(EquipmentSet)
class EquipmentSetAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)


@admin.register(ItemTier)
class ItemTierAdmin(admin.ModelAdmin):
    autocomplete_fields = ['item']


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    filter_horizontal = ('mastery',)


@admin.register(ItemSpec)
class ItemSpecAdmin(admin.ModelAdmin):
    autocomplete_fields = ['item']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    ordering = ['item_name']
    search_fields = ['item_name']


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    ordering = ['item_type']
    search_fields = ['item_type']


@admin.register(EfficientItemResult)
class EfficientItemResultAdmin(admin.ModelAdmin):
    readonly_fields = ['time_saved']


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    pass
