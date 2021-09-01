import importlib


def required_class_attributes_checker(cls, *attrs: str):
    for attr_name in attrs:
        try:
            getattr(cls, attr_name)
        except AttributeError:
            raise TypeError(f'Provide `{attr_name}` attribute in {cls.__module__}.{cls.__name__}')


def import_attribute(path):
    assert isinstance(path, str)
    pkg, attr = path.rsplit(".", 1)
    ret = getattr(importlib.import_module(pkg), attr)
    return ret
