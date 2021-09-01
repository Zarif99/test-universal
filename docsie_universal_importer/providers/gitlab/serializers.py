from rest_framework import serializers

from docsie_universal_importer.providers.base import StorageTreeRequestSerializer, DownloaderRequestSerializer


class GitlabStorageTreeRequestSerializer(StorageTreeRequestSerializer):
    repo = serializers.CharField()


class GitlabDownloaderSerializer(DownloaderRequestSerializer):
    repo = serializers.CharField()
