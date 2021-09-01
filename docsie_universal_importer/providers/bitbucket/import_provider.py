import os
from dataclasses import dataclass
from pathlib import Path

from swag_auth.bitbucket.connectors import BitbucketAPIConnector

from docsie_universal_importer.providers.base import (
    File, StorageViewer, StorageTree,
    Downloader, Provider, DownloaderAdapter,
    StorageViewerAdapter
)
from .serializers import BitbucketStorageTreeRequestSerializer, BitbucketDownloaderSerializer


@dataclass
class BitbucketFile(File):
    path: str

    @classmethod
    def from_external(cls, file_obj, **kwargs):
        name = Path(file_obj['path']).name

        return cls(name=name, path=file_obj['path'])


class BitbucketRepository:
    def __init__(self, client: BitbucketAPIConnector, name: str):
        self.name = name
        self.client = client

    def get_content(self, path: str, ref: str):
        return self.client.client.get_file_content(self.name, path, ref)

    def get_default_branch(self) -> str:
        return self.client.get_default_branch(self.name)


class BitbucketStorageViewer(StorageViewer):
    file_cls = BitbucketFile

    def __init__(self, repo):
        self.repo = repo

    def init_storage_tree(self) -> StorageTree:
        return StorageTree(self.repo.name)

    def get_contents(self, repo, path, branch):
        return repo.client.get_file_content(self.repo.name, path, branch)

    def get_external_files(self):
        branch = self.repo.get_default_branch()
        contents = self.get_contents(self.repo, "", branch)

        while contents:
            file_obj = contents.pop(0)
            if file_obj['type'] == "commit_directory":
                contents.extend(self.get_contents(self.repo, file_obj['path'], branch=branch))
            else:
                yield os.path.dirname(file_obj["path"]), file_obj


class BitbucketDownloader(Downloader):
    file_cls = BitbucketFile

    def __init__(self, repo):
        self.repo = repo

    def download_file(self, file: BitbucketFile):
        return self.repo.get_content(file.path, self.repo.get_default_branch())


class BitbucketDownloaderAdapter(DownloaderAdapter):
    adapted_cls = BitbucketDownloader
    request_serializer_cls = BitbucketDownloaderSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']
        repo_name = validated_data['repo']

        client = BitbucketAPIConnector(token)

        return {'repo': BitbucketRepository(client, repo_name)}


class BitbucketStorageViewerAdapter(StorageViewerAdapter):
    adapted_cls = BitbucketStorageViewer
    request_serializer_cls = BitbucketStorageTreeRequestSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']
        repo_name = validated_data['repo']

        client = BitbucketAPIConnector(token)

        return {'repo': BitbucketRepository(client, repo_name)}


class BitbucketProvider(Provider):
    id = 'bitbucket'

    storage_viewer_adapter_cls = BitbucketStorageViewerAdapter
    downloader_adapter_cls = BitbucketDownloaderAdapter


provider_classes = [BitbucketProvider]
