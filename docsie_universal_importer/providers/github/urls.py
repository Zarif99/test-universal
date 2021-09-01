from docsie_universal_importer.providers.base.urls import default_urlpatterns

from .import_provider import GithubProvider

urlpatterns = default_urlpatterns(GithubProvider)
