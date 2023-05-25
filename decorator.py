
import js
from js import React
from typing import Protocol, List, Dict, Any, Type
from collections.abc import Iterable
from js import JSON

from pyodide.ffi import create_proxy, JsProxy

from react.component import Component

CHILDREN_KEY = 'children'

class FunctionComponent(Protocol):
    def __call__(*children: List[JsProxy], **props: Dict[str, Any]) -> JsProxy:
        pass


def component(component_func: FunctionComponent) -> Type[Component]:
        @create_proxy
        def decorated(props, component_ref) -> JsProxy:
                props = dict(js.Object.entries(props))

                try:
                        children = props[CHILDREN_KEY]
                        # React passes single child raw.
                        # Single list child not currently supported.
                        if not isinstance(children, Iterable): 
                                children = [children]
                        del props[CHILDREN_KEY]
                except KeyError:
                        children = []
                
                
                children = [child.to_py() if isinstance(child, JsProxy) else child 
                            for child in children] 
                return component_func(*children, **props)


        return type(component_func.__name__, (Component,), {'_wrapped': decorated})