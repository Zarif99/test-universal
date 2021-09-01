from docsie_universal_importer.providers.base import StorageTreeView, ImporterView
from .import_provider import GitlabProvider

storage_view = StorageTreeView.provider_view(GitlabProvider)
importer_view = ImporterView.provider_view(GitlabProvider)
