import math
from typing import Dict, Any, List, Union, Callable
from abc import abstractmethod, ABC

import js
from js import React
from js import JSON

import pyodide
from pyodide.ffi import create_proxy, to_js, JsProxy


def _make_js_object(raw_dict: Dict[str, Any]) -> JsProxy:
    return js.Object.fromEntries(to_js(raw_dict))


def _to_camel_case(snake_case: str) -> str:
    components = snake_case.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class _Props:
    def __init__(self, **props: Dict[str, Any]):
        self.props = props

    def to_js(self) -> JsProxy:
        return _make_js_object(
            {_to_camel_case(key): create_proxy(value) if callable(value) else value
             for key, value in self.props.items()}
        )


class Component(ABC):
    def __init__(self, **props: Dict[str, Any]):
        self.props = _Props(**props)
        
    @property
    @abstractmethod
    def _wrapped(self) -> Union[callable, str, JsProxy]:
        pass

    def __call__(self, *children: List[JsProxy]) -> JsProxy:
        print(f'Creating {self.__class__.__name__} component...')
        proxy_children = [create_proxy(child) for child in children]
        result = React.createElement(
            self._wrapped,
            self.props.to_js(),
            *children
        )
        return result

    def __getitem__(self, children: List[JsProxy] | JsProxy):
        if not isinstance(children, tuple):
            children = (children,)
        return self(*children)



    def __class_getitem__(cls, children: List[JsProxy] | JsProxy):
        if not isinstance(children, tuple):
            children = (children,)
        return cls()(*children)
