import os
from dataclasses import dataclass
from pathlib import Path

from gitlab import Gitlab

from docsie_universal_importer.providers.base import (
    File, StorageViewer, StorageTree,
    Downloader, Provider, DownloaderAdapter,
    StorageViewerAdapter
)
from .serializers import GitlabDownloaderSerializer, GitlabStorageTreeRequestSerializer


@dataclass
class GitlabFile(File):
    path: str

    @classmethod
    def from_external(cls, file_obj, **kwargs):
        name = Path(file_obj['path']).name

        return cls(name=name, path=file_obj['path'])


class GitlabStorageViewer(StorageViewer):
    file_cls = GitlabFile

    def __init__(self, repo):
        self.repo = repo

    def init_storage_tree(self) -> StorageTree:
        return StorageTree(f"{self.repo.owner['username']}/{self.repo.name}")

    def get_contents(self, repo, path, branch):
        return repo.repository_tree(path, branch)

    def get_external_files(self):
        branch = self.repo.default_branch
        contents = self.get_contents(self.repo, "", branch=branch)
        while contents:
            file_obj = contents.pop(0)
            if file_obj['type'] == "tree":
                contents.extend(self.get_contents(self.repo, file_obj['path'], branch))
            else:
                yield os.path.dirname(file_obj['path']), file_obj


class GitlabDownloader(Downloader):
    file_cls = GitlabFile

    def __init__(self, repo):
        self.repo = repo

    def get_file_content(self, repo, path, ref):
        """
        Return content of the given path file
        :param repo:
        :param path:
        :param ref:
        :return:
        """
        return repo.files.get(file_path=path.path, ref=ref).decode()

    def download_file(self, file: GitlabFile):
        return self.get_file_content(repo=self.repo, path=file, ref=self.repo.default_branch)


class GitlabDownloaderAdapter(DownloaderAdapter):
    adapted_cls = GitlabDownloader
    request_serializer_cls = GitlabDownloaderSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']
        repo_name = validated_data['repo']
        client = Gitlab("https://gitlab.com", oauth_token=token)

        return {'repo': client.projects.get(repo_name)}


class GitlabStorageViewerAdapter(StorageViewerAdapter):
    adapted_cls = GitlabStorageViewer
    request_serializer_cls = GitlabStorageTreeRequestSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']
        repo_name = validated_data['repo']

        client = Gitlab("https://gitlab.com", oauth_token=token)

        return {'repo': client.projects.get(repo_name)}


class GitlabProvider(Provider):
    id = 'gitlab'

    storage_viewer_adapter_cls = GitlabStorageViewerAdapter
    downloader_adapter_cls = GitlabDownloaderAdapter


provider_classes = [GitlabProvider]
