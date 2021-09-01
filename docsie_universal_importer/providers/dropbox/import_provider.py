import os
from dataclasses import dataclass

from dropbox import Dropbox, files

from docsie_universal_importer.providers.base import (
    File, StorageViewer, StorageTree,
    Downloader, Provider, DownloaderAdapter,
    StorageViewerAdapter
)
from .serializers import DropboxStorageTreeRequestSerializer, DropboxDownloaderSerializer


@dataclass
class DropboxFile(File):
    path: str

    @classmethod
    def from_external(cls, file_obj, **kwargs):

        return cls(name=file_obj.name, path=file_obj.path_lower)


class DropboxStorageViewer(StorageViewer):
    file_cls = DropboxFile

    def __init__(self, dropbox_client):
        self.dropbox_client = dropbox_client

    def init_storage_tree(self) -> StorageTree:
        return StorageTree(".")

    def get_external_files(self):
        contents = self.dropbox_client.files_list_folder("").entries

        while contents:
            file_obj = contents.pop(0)
            if isinstance(file_obj, files.FolderMetadata):
                contents.extend(self.dropbox_client.files_list_folder(file_obj.path_lower).entries)
            else:
                yield os.path.dirname(file_obj.path_lower), file_obj


class DropboxDownloader(Downloader):
    file_cls = DropboxFile

    def __init__(self, dropbox_client):
        self.dropbox_client = dropbox_client

    def download_file(self, file: DropboxFile):
        metadata, response = self.dropbox_client.files_download(path=file.path)
        return response.content


class DropboxDownloaderAdapter(DownloaderAdapter):
    adapted_cls = DropboxDownloader
    request_serializer_cls = DropboxDownloaderSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']

        client = Dropbox(token)

        return {'dropbox_client': client}


class DropboxStorageViewerAdapter(StorageViewerAdapter):
    adapted_cls = DropboxStorageViewer
    request_serializer_cls = DropboxStorageTreeRequestSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']

        client = Dropbox(token)

        return {'dropbox_client': client}


class DropboxProvider(Provider):
    id = 'dropbox'

    storage_viewer_adapter_cls = DropboxStorageViewerAdapter
    downloader_adapter_cls = DropboxDownloaderAdapter


provider_classes = [DropboxProvider]
