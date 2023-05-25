from pyodide.ffi import JsProxy
from react.component import Component
from react.is_react_component import is_react_component
from types import ModuleType
from typing import Any

import sys

class ComponentsModule(ModuleType):
    def __init__(self, name: str, wrapped: JsProxy):
        super().__init__(name)
        self._wrapped = wrapped

    def __getattr__(self, component_name: str) -> Any:
        attr = getattr(self._wrapped, component_name, None)
        if attr is not None and is_react_component(attr):
            return type(component_name, (Component,), {'_wrapped': attr})
        raise AttributeError(f'Module \'{self.__name__}\' has no component attribute \'{component_name}\'')


def load_module(js_module: JsProxy, name: str):
    module =  ComponentsModule(name, js_module)
    sys.modules[f'{__name__}.{name}'] = module
    setattr(sys.modules[f'{__name__}'], name, module)


def __getattr__(tag_name: str) -> Any:
    return type(tag_name, (Component,), {'_wrapped': tag_name})


__all__ = ['load_module']