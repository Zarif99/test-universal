from docsie_universal_importer.providers.base import StorageTreeView, ImporterView
from .import_provider import BoxProvider

storage_view = StorageTreeView.provider_view(BoxProvider)
importer_view = ImporterView.provider_view(BoxProvider)
