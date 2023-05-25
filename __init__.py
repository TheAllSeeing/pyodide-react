
from react.component import Component

from js import React as __React
from typing import Any as __Any
from react.case_converter import to_camel_case as __to_camel_case
def __getattr__(attr: str):
        try:
                return getattr(__React, attr)
        except AttributeError:
                return getattr(__React, __to_camel_case(attr))