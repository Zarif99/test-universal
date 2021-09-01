import os
from dataclasses import dataclass
from pathlib import Path

from boxsdk import OAuth2, Client
from django.conf import settings

from docsie_universal_importer.providers.base import (
    File, StorageViewer, StorageTree,
    Downloader, Provider, DownloaderAdapter,
    StorageViewerAdapter
)
from .serializers import BoxStorageTreeRequestSerializer, BoxDownloaderSerializer


@dataclass
class BoxFile(File):
    id: str

    @classmethod
    def from_external(cls, file_obj, **kwargs):
        name = Path(file_obj.name).name

        return cls(name=name, id=file_obj.id)


class BoxStorageViewer(StorageViewer):
    file_cls = BoxFile

    def __init__(self, box_client):
        self.box_client = box_client

    def init_storage_tree(self) -> StorageTree:
        return StorageTree(".")

    def get_external_files(self):
        contents = list(self.box_client.folder(folder_id=0).get_items())
        while contents:
            file_obj = contents.pop(0)
            if file_obj.type == "folder":
                ans = []
                files = list(self.box_client.folder(folder_id=file_obj.id).get_items())
                for file in files:
                    file.name = f"{file_obj.name}/{file.name}"
                    ans.append(file)
                contents.extend(files)
            else:
                yield os.path.dirname(file_obj.name), file_obj


class BoxDownloader(Downloader):
    file_cls = BoxFile

    def __init__(self, box_client):
        self.box_client = box_client

    def download_file(self, file: BoxFile):
        return self.box_client.file(file.id).content()


class BoxOauth2Client(Client):
    def __init__(self, token, *args, **kwargs):
        auth = OAuth2(
            client_id=settings.SWAGAUTH_SETTINGS['box']['APP']['client_id'],
            client_secret=settings.SWAGAUTH_SETTINGS['box']['APP']['secret'],
            access_token=token,
        )
        super().__init__(oauth=auth)


class BoxDownloaderAdapter(DownloaderAdapter):
    adapted_cls = BoxDownloader
    request_serializer_cls = BoxDownloaderSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']

        client = BoxOauth2Client(token)

        return {'box_client': client}


class BoxStorageViewerAdapter(StorageViewerAdapter):
    adapted_cls = BoxStorageViewer
    request_serializer_cls = BoxStorageTreeRequestSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']

        client = BoxOauth2Client(token)

        return {'box_client': client}


class BoxProvider(Provider):
    id = 'box'

    storage_viewer_adapter_cls = BoxStorageViewerAdapter
    downloader_adapter_cls = BoxDownloaderAdapter


provider_classes = [BoxProvider]
