import os
from dataclasses import dataclass

import requests
from github import ContentFile

from docsie_universal_importer.providers.base import (
    File, StorageViewer, StorageTree,
    Downloader, Provider, DownloaderAdapter,
    StorageViewerAdapter
)
from .serializers import ConfluenceStorageTreeRequestSerializer, ConfluenceDownloaderSerializer


class ConfluenceConnector:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }
        self.cloud_id = self._get_cloud_id()
        self.base_url = f'https://api.atlassian.com/ex/confluence/{self.cloud_id}/rest/api/content'

    def _get_cloud_id(self):
        r = requests.get('https://api.atlassian.com/oauth/token/accessible-resources', headers=self.headers)
        return r.json()[0]['id']

    def _request(self, endpoint: str):
        if not endpoint[:1] == '/':  # adding slash pre endpoint if you forgot adding this
            endpoint = '/' + endpoint

        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers)

        return response

    def get_page_content(self, page_id):
        endpoint = f'{page_id}?expand=body.storage'
        response = self._request(endpoint)

        return response.json()['body']['storage']['value']

    def list_pages_ids(self, page_id='/'):
        response = self._request(page_id).json()  # request to the base url
        return response.get('results')


@dataclass
class ConfluenceFile(File):
    id: str

    @classmethod
    def from_external(cls, file_obj: ContentFile, **kwargs):
        name = file_obj.get('title')

        return cls(name=name, id=file_obj.get('id'))


class ConfluenceStorageViewer(StorageViewer):
    file_cls = ConfluenceFile

    def __init__(self, client: ConfluenceConnector):
        self.client = client

    def init_storage_tree(self) -> StorageTree:
        return StorageTree('.')

    def get_external_files(self):
        pages_ids = self.client.list_pages_ids()
        while pages_ids:
            file_obj = pages_ids.pop(0)

            yield os.path.dirname(file_obj.get('title')), file_obj


class ConfluenceDownloader(Downloader):
    file_cls = ConfluenceFile

    def __init__(self, client: ConfluenceConnector):
        self.client = client

    def download_file(self, file: ConfluenceFile):
        return self.client.get_page_content(file.id)


class ConfluenceDownloaderAdapter(DownloaderAdapter):
    adapted_cls = ConfluenceDownloader
    request_serializer_cls = ConfluenceDownloaderSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']

        client = ConfluenceConnector(token=token)

        return {'client': client}


class ConfluenceStorageViewerAdapter(StorageViewerAdapter):
    adapted_cls = ConfluenceStorageViewer
    request_serializer_cls = ConfluenceStorageTreeRequestSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']

        client = ConfluenceConnector(token=token)

        return {'client': client}


class ConfluenceProvider(Provider):
    id = 'confluence'

    storage_viewer_adapter_cls = ConfluenceStorageViewerAdapter
    downloader_adapter_cls = ConfluenceDownloaderAdapter


provider_classes = [ConfluenceProvider]
