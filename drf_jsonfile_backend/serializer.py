__author__ = 'Imam Omar Mochtar (iomarmochtar@gmail.com)'
__email__ = 'iomarmochtar@gmail.com'

from rest_framework import serializers
from .commons import Obj


class JsonFileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        return Obj(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
