from importlib import import_module

from docsie_universal_importer import providers

urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + ".urls")
    except ImportError:
        continue

    urlpatterns.extend(getattr(prov_mod, "urlpatterns", []))
