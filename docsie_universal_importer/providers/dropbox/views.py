from docsie_universal_importer.providers.base import StorageTreeView, ImporterView
from .import_provider import DropboxProvider

storage_view = StorageTreeView.provider_view(DropboxProvider)
importer_view = ImporterView.provider_view(DropboxProvider)
