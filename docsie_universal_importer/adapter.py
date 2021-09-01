from rest_framework import serializers

from docsie_universal_importer.import_adapter import ImportAdapter


class MyImportAdapter(ImportAdapter):
    def import_content(self, file, content, **kwargs):
        print(file)
        print(content)
        print(kwargs)


class ImportParamsSerializer(serializers.Serializer):
    type = serializers.CharField()
