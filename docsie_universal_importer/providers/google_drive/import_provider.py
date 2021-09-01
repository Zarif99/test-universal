import io
import os
from dataclasses import dataclass
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from docsie_universal_importer.providers.base import (
    File, StorageViewer, StorageTree,
    Downloader, Provider, DownloaderAdapter,
    StorageViewerAdapter
)
from .serializers import GoogleDriveStorageTreeRequestSerializer, GoogleDriveDownloaderSerializer


@dataclass
class GoogleDriveFile(File):
    id: str

    @classmethod
    def from_external(cls, file_obj, **kwargs):
        name = Path(file_obj['name']).name
        return cls(name=name, id=file_obj['id'])


class GoogleDriveOauth2Client:
    def __init__(self, token, *args, **kwargs):
        credentials = Credentials(token=token)

        self.client = build('drive', 'v3', credentials=credentials)

    def __getattr__(self, item):
        return getattr(self.client, item)


class GoogleDriveStorageViewer(StorageViewer):
    file_cls = GoogleDriveFile
    folder_mimetype = 'application/vnd.google-apps.folder'

    def __init__(self, google_drive_client):
        self.google_drive_client = google_drive_client

    def init_storage_tree(self) -> StorageTree:
        return StorageTree(".")

    def get_files(self, name=None, *, is_folder=None, parent=None,
                  order_by='folder,name,createdTime'):

        q = []
        if name is not None:
            q.append("name = '{}'".format(name.replace("'", "\\'")))
        if is_folder is not None:
            q.append("mimeType {} '{}'".format('=' if is_folder else '!=', self.folder_mimetype))
        if parent is not None:
            q.append("'{}' in parents".format(parent.replace("'", "\\'")))
        params = {'pageToken': None, 'orderBy': order_by}
        if q:
            params['q'] = ' and '.join(q)
        while True:
            response = self.google_drive_client.files().list(**params).execute()
            for f in response['files']:
                yield f
            try:
                params['pageToken'] = response['nextPageToken']
            except KeyError:
                return

    def walk(self, top='root', *, by_name: bool = False):
        if top:
            top = self.google_drive_client.files().get(fileId=top).execute()
        else:
            top = self.google_drive_client.files().get(fileId="root").execute()
        stack = [((top['name'],), top)]
        while stack:
            path, top = stack.pop()
            dirs, files = is_file = [], []
            for f in self.get_files(parent=top['id']):
                is_file[f['mimeType'] != self.folder_mimetype].append(f)
            yield path, top, dirs, files
            if dirs:
                stack.extend((path + (d['name'],), d) for d in dirs)

    def get_external_files(self):
        kwargs = {'top': 'root', 'by_name': True}
        for path, root, dirs, files in self.walk(**kwargs):
            for file in files:
                parent = '/'.join(path[1:]).lstrip('/')
                if parent:
                    file_path = f"{parent}/{file.get('name')}"
                else:
                    file_path = file.get('name')
                file_id = file.get('id')
                file_obj = {
                    'name': file_path,
                    'id': file_id
                }
                yield os.path.dirname(file_obj['name']), file_obj


class GoogleDriveDownloader(Downloader):
    file_cls = GoogleDriveFile

    def __init__(self, google_drive_client):
        self.google_drive_client = google_drive_client

    def download_file(self, file: GoogleDriveFile):
        file = self.google_drive_client.files().get_media(fileId=file.id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, file)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        return fh.getvalue()


class GoogleDriveDownloaderAdapter(DownloaderAdapter):
    adapted_cls = GoogleDriveDownloader
    request_serializer_cls = GoogleDriveDownloaderSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']

        client = GoogleDriveOauth2Client(token)

        return {'google_drive_client': client}


class GoogleDriveStorageViewerAdapter(StorageViewerAdapter):
    adapted_cls = GoogleDriveStorageViewer
    request_serializer_cls = GoogleDriveStorageTreeRequestSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']

        client = GoogleDriveOauth2Client(token)

        return {'google_drive_client': client}


class GoogleDriveProvider(Provider):
    id = 'google'

    storage_viewer_adapter_cls = GoogleDriveStorageViewerAdapter
    downloader_adapter_cls = GoogleDriveDownloaderAdapter


provider_classes = [GoogleDriveProvider]
