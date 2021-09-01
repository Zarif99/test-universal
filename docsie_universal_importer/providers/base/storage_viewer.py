from abc import ABC, abstractmethod
from typing import Any, Type, Tuple, Generator

from docsie_universal_importer.utils import required_class_attributes_checker
from .storage_tree import File, StorageTree


class StorageViewer(ABC):
    file_cls: Type[File] = None

    @abstractmethod
    def init_storage_tree(self) -> StorageTree:
        pass

    @abstractmethod
    def get_external_files(self) -> Generator[Tuple[str, Any], None, None]:
        pass

    def get_storage_tree(self) -> StorageTree:
        storage_tree = self.init_storage_tree()

        for path, file_obj in self.get_external_files():
            file = self.get_file_from_external(file_obj)

            storage_tree.add_file(path, file)

        return storage_tree

    def get_file_from_external(self, file_obj: Any) -> File:
        required_class_attributes_checker(self.__class__, 'file_cls')

        return self.file_cls.from_external(file_obj)
