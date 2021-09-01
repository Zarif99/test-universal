from docsie_universal_importer.providers.base import StorageTreeView, ImporterView
from .import_provider import GoogleDriveProvider

storage_view = StorageTreeView.provider_view(GoogleDriveProvider)
importer_view = ImporterView.provider_view(GoogleDriveProvider)
