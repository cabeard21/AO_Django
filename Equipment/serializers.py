from rest_framework import serializers

from .models import ExcludedItem


class ExcludedItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExcludedItem
        fields = [
            'item_name',
            'tier',
            'quality',
            'price'
        ]
