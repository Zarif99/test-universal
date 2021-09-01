from docsie_universal_importer.providers.base.urls import default_urlpatterns

from .import_provider import ConfluenceProvider

urlpatterns = default_urlpatterns(ConfluenceProvider)
