from rest_framework import serializers
from swag_auth.models import ConnectorToken


class BaseRequestSerializer(serializers.Serializer):
    token = serializers.PrimaryKeyRelatedField(queryset=ConnectorToken.objects.all())

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['token'] = instance['token'].token

        return data


class StorageTreeRequestSerializer(BaseRequestSerializer):
    pass


class DownloaderRequestSerializer(BaseRequestSerializer):
    files = serializers.ListField(child=serializers.DictField())
