from django.contrib import admin

from .models import *

@admin.register(EquipmentSet)
class EquipmentSetAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)

admin.site.register(ItemTier)
admin.site.register(Character)
admin.site.register(ItemTypeSpec)

admin.site.register(Item)
admin.site.register(ItemType)
