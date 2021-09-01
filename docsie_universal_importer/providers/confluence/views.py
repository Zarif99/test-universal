from docsie_universal_importer.providers.base import StorageTreeView, ImporterView
from .import_provider import ConfluenceProvider

storage_view = StorageTreeView.provider_view(ConfluenceProvider)
importer_view = ImporterView.provider_view(ConfluenceProvider)
