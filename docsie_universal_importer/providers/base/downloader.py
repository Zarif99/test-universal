from abc import abstractmethod
from typing import Union, Type

from docsie_universal_importer.utils import required_class_attributes_checker
from .storage_tree import File


class Downloader:
    file_cls: Type[File] = None

    @abstractmethod
    def download_file(self, file: File) -> Union[str, bytes]:
        pass

    def get_file_from_kwargs(self, **file_kwargs) -> File:
        required_class_attributes_checker(self.__class__, 'file_cls')

        return self.file_cls(**file_kwargs)
