from docsie_universal_importer.providers.base.urls import default_urlpatterns

from .import_provider import BitbucketProvider

urlpatterns = default_urlpatterns(BitbucketProvider)
