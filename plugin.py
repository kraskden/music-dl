import importlib
import inspect
import pkgutil
from pathlib import Path

from downloader.downloader import Downloader
from source.source import Source


def plugin(cls):
    cls._PLUGIN_ = True
    return cls


def load_source(location, *args, **kwargs) -> Source:
    for name in _get_module_names('source'):
        try:
            module = _load_module('source', name)
            source: Source = _load_plugin(module, Source, *args, **kwargs)
            if source.match(location):
                return source
        except ValueError:
            continue
    raise ValueError(f"No module is available for {location}")


def get_plugins_names(base_package, base_class):
    result = []
    for name in _get_module_names(base_package):
        try:
            module = _load_module(base_package, name)
            cls = _get_plugin(module, base_class)
            result.append(name)
        except ValueError:
            continue
    return result


def load_dl(name, *args, **kwargs) -> Downloader:
    return _load_plugin(_load_module('downloader', name), Downloader, *args, **kwargs)


def _get_module_names(component):
    directory = (Path(__file__)).parent.absolute() / component
    return [name for _, name, _ in pkgutil.iter_modules([str(directory)])]


def _load_module(package, name):
    return importlib.import_module(f'{package}.{name}', '.')


def _load_plugin(module, base_class, *args, **kwargs):
    cls = _get_plugin(module, base_class)
    return cls(*args, **kwargs)


def _get_plugin(module, base_class):
    classes = inspect.getmembers(module, inspect.isclass)
    for name, cls in classes:
        if issubclass(cls, base_class) and hasattr(cls, '_PLUGIN_'):
            return cls
    raise ValueError(f'Module {module} is not loaded')
