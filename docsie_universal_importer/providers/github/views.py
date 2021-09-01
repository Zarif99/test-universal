from docsie_universal_importer.providers.base import StorageTreeView, ImporterView
from .import_provider import GithubProvider

storage_view = StorageTreeView.provider_view(GithubProvider)
importer_view = ImporterView.provider_view(GithubProvider)
