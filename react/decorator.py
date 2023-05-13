
import js
from js import React
from typing import Protocol, List, Dict, Any, Type
from collections.abc import Iterable

from pyodide.ffi import create_proxy, JsProxy

from src.react.component import Component

CHILDREN_KEY = 'children'

class FunctionComponent(Protocol):
    def __call__(*children: List[JsProxy], **props: Dict[str, Any]) -> JsProxy:
        pass


def component(component_func: FunctionComponent) -> Type[Component]:
        @create_proxy
        def decorated(props, component_ref) -> JsProxy:
                props = dict(js.Object.entries(props))
                try:
                        children = React.Children.toArray(props[CHILDREN_KEY])
                        del props[CHILDREN_KEY]
                except KeyError:
                        children = []
                
                return component_func(*children, **props)


        return type(component_func.__name__, (Component,), {'_wrapped': create_proxy(decorated)})