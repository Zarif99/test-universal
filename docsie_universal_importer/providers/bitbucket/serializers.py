from rest_framework import serializers

from docsie_universal_importer.providers.base import StorageTreeRequestSerializer, DownloaderRequestSerializer


class BitbucketStorageTreeRequestSerializer(StorageTreeRequestSerializer):
    repo = serializers.CharField()


class BitbucketDownloaderSerializer(DownloaderRequestSerializer):
    repo = serializers.CharField()
