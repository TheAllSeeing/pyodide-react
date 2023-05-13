from src.react.component import Component

import js.MaterialUI as mui
class Button(Component):
    _wrapped = mui.Button


def __getattr__(tag_name: str):
    return type(tag_name, (Component,), {'_wrapped': tag_name})