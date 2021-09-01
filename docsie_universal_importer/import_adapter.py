from abc import ABC, abstractmethod
from typing import Union

from .providers.base.storage_tree import File


class ImportAdapter(ABC):
    @abstractmethod
    def import_content(self, request, file: File, content: Union[str, bytes], **kwargs):
        pass
