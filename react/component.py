import math
from typing import Dict, Any, List, Union, Callable
from abc import abstractmethod, ABC

import js
from js import React

import pyodide
from pyodide.ffi import create_proxy, to_js, JsProxy


def _make_js_object(raw_dict: Dict[str, Any]) -> Any:
    return js.Object.fromEntries(to_js(raw_dict))


def _to_camel_case(snake_case: str) -> str:
    components = snake_case.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class _Props:
    def __init__(self, **props):
        self.props = props

    def to_js(self):
        return _make_js_object(
            {_to_camel_case(key): create_proxy(value) if callable(value) else value
             for key, value in self.props.items()}
        )


class Component(ABC):
    def __init__(self, **props):
        self.props = _Props(**props)
        
    @property
    @abstractmethod
    def _wrapped(self) -> Union[callable, str, JsProxy]:
        pass

    def __call__(self, *children):
        return React.createElement(
            self._wrapped,
            self.props.to_js(),
            *children
        )

    __getitem__ = __call__


    def __class_getitem__(cls, *children):
        return cls()(*children)
