import importlib
from typing import TypeVar
from types import ModuleType

from ..neko.integrations import neko_config


T = TypeVar('T')


def apply_replace(obj: T) -> T:
    if isinstance(obj, ModuleType):
        module = obj.__package__
        if obj.__name__ == obj.__package__:
            module = module.split('.')[0]
        name = obj.__name__.removeprefix(module).removeprefix('.')
    elif issubclass(obj, object):
        module = obj.__module__
        name = obj.__name__
    else:
        raise ImportError(f'Cannot apply import patches to type {type(obj)}')

    try:
        return importlib.import_module(
            neko_config.connections[module.split('.')[0]]
            + module.removeprefix(module.split('.')[0])
        ).__getattribute__(name)
    except (AttributeError, KeyError):
        raise ImportError(
            f'No standard--implementation connection for '
            f'{module.split(".")[0]}'
        )
