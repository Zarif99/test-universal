from docsie_universal_importer.providers.base import StorageTreeView, ImporterView
from .import_provider import BitbucketProvider

storage_view = StorageTreeView.provider_view(BitbucketProvider)
importer_view = ImporterView.provider_view(BitbucketProvider)
