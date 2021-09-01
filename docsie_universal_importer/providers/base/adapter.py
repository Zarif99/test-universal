import json
from abc import ABC, abstractmethod
from typing import Type, Dict, Any, Generator

from rest_framework.serializers import Serializer

from docsie_universal_importer.providers.base import Downloader, StorageViewer, File
from docsie_universal_importer.utils import required_class_attributes_checker
from .serializers import DownloaderRequestSerializer, StorageTreeRequestSerializer


class Adapter(ABC):
    request_serializer_cls: Type[Serializer] = None

    adapted_cls: Type[Any] = None

    def __init__(self, request):
        required_class_attributes_checker(self.__class__, 'request_serializer_cls', 'adapted_cls')

        self.request = request

    @property
    def adapted(self):
        return self.get_adapted()

    def get_adapted(self):
        serializer = self.get_serializer()
        init_kwargs = self.get_adapted_init_kwargs(serializer.data)

        adapted_cls = self.get_adapted_cls()

        return adapted_cls(**init_kwargs)

    def get_serializer(self) -> Serializer:
        request_data = self.get_request_data(self.request)
        serializer_cls = self.get_serializer_class()

        serializer = serializer_cls(data=request_data)
        serializer.is_valid(raise_exception=True)

        return serializer

    @abstractmethod
    def get_adapted_init_kwargs(self, validated_data: dict) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_request_data(self, request):
        pass

    def get_serializer_class(self) -> Type[Serializer]:
        return self.request_serializer_cls

    def get_adapted_cls(self):
        return self.adapted_cls


class StorageViewerAdapter(Adapter):
    request_serializer_cls: Type[StorageTreeRequestSerializer] = None
    adapted_cls: Type[StorageViewer] = None

    def get_request_data(self, request):
        return request.GET.copy()


class DownloaderAdapter(Adapter):
    request_serializer_cls: Type[DownloaderRequestSerializer] = None
    adapted_cls: Type[Downloader] = None

    def get_request_data(self, request):
        return json.loads(request.body)

    def get_files(self) -> Generator[File, None, None]:
        for file_kwargs in self.get_files_data():
            yield self.adapted.get_file_from_kwargs(**file_kwargs)

    def get_files_data(self):
        serializer = self.get_serializer()

        return serializer.data['files']
