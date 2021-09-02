from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Union, Any, List


@dataclass
class File(ABC):
    name: str
    type: str = field(init=False, default='file')

    @classmethod
    @abstractmethod
    def from_external(cls, file_obj: Any, **kwargs):
        pass

    def to_dict(self):
        data = asdict(self)

        return {data['name']: data}


@dataclass
class StorageTree:
    name: str

    type: str = field(init=False, default='directory')
    children: List[Union['StorageTree', File]] = field(default_factory=list)

    def add_file(self, path, file: File):
        current_path = self.children
        for bit in Path(path).parts:
            # Get the first dict which contains a `bit` key.
            folder = None
            for existing_tree in current_path:
                if isinstance(existing_tree, StorageTree) and existing_tree.name == bit:
                    folder = existing_tree
                    break

            if folder is None:
                folder = StorageTree(bit)
                current_path.append(folder)

            current_path = folder.children

        # Do not add a file if it already exists
        if file not in current_path:
            current_path.append(file)

    def get_files(self):
        files: List[File] = []

        for child in self.children:
            if isinstance(child, File):
                files.append(child)
            else:
                files.extend(child.get_files())

        return files

    def to_dict(self):
        storage_tree = {
            self.name: {
                'type': self.type,
                'children': {}
            }
        }

        for child in self.children:
            child_data = child.to_dict()

            storage_tree[self.name]['children'].update(child_data)

        return storage_tree
