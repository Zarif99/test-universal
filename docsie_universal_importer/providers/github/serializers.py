from rest_framework import serializers

from docsie_universal_importer.providers.base import StorageTreeRequestSerializer, DownloaderRequestSerializer


class GithubStorageTreeRequestSerializer(StorageTreeRequestSerializer):
    repo = serializers.CharField()


class GithubDownloaderSerializer(DownloaderRequestSerializer):
    repo = serializers.CharField()
