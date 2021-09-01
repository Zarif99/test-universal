from docsie_universal_importer.providers.base.urls import default_urlpatterns

from .import_provider import GitlabProvider

urlpatterns = default_urlpatterns(GitlabProvider)
