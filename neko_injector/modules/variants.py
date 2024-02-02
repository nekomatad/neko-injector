from .applyer import apply_replace

from typing import Iterable, Type, TypeVar
from types import ModuleType


T = TypeVar('T')


def inject_object(*objects) -> None:
    for obj in objects:
        new = apply_replace(obj)
        for attr, value in new.__dict__.items():
            try:
                setattr(obj, attr, getattr(new, attr))
            except AttributeError:
                continue


def get_injected_object(*objects: Type[T]) -> Iterable[T]:
    return [apply_replace(obj) for obj in objects]


def inject_module(mod: ModuleType) -> None:
    try:
        inject_object(*getattr(mod, '__replacements__'))
    except AttributeError:
        raise ImportError(f'Module {mod.__name__} does not define a list of '
                          f'replacements, it cannot be patched')
    except ModuleNotFoundError:
        raise ImportError(f'The implementation presented in the config does not comply '
                          f'with the structure of the standard')


def inject_modules(modules: list[ModuleType]) -> None:
    for module in modules:
        inject_module(module)
