import sys


class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, default):
        from django.conf import settings

        return getattr(settings, self.prefix + name, default)

    @property
    def PROVIDERS(self):
        """Provider specific settings"""
        return self._setting("PROVIDERS", {})

    @property
    def IMPORT_ADAPTER(self):
        return self._setting("ADAPTER", '')

    @property
    def IMPORT_SERIALIZER(self):
        return self._setting('SERIALIZER', '')


app_settings = AppSettings("UNIVERSAL_DOC_IMPORTER_")
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
