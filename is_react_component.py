from js import Symbol
from pyodide.ffi import JsProxy

make_symbol = getattr(Symbol, 'for')

REACT_ELEMENT_TYPE = make_symbol('react.element')
REACT_PORTAL_TYPE = make_symbol('react.portal')
REACT_FRAGMENT_TYPE = make_symbol('react.fragment')
REACT_STRICT_MODE_TYPE = make_symbol('react.strict_mode')
REACT_PROFILER_TYPE = make_symbol('react.profiler')
REACT_PROVIDER_TYPE = make_symbol('react.provider')
REACT_CONTEXT_TYPE = make_symbol('react.context')
REACT_SERVER_CONTEXT_TYPE = make_symbol('react.server_context')
REACT_FORWARD_REF_TYPE = make_symbol('react.forward_ref')
REACT_SUSPENSE_TYPE = make_symbol('react.suspense')
REACT_SUSPENSE_LIST_TYPE = make_symbol('react.suspense_list')
REACT_MEMO_TYPE = make_symbol('react.memo')
REACT_LAZY_TYPE = make_symbol('react.lazy')
REACT_OFFSCREEN_TYPE = make_symbol('react.offscreen')
REACT_MODULE_REFERENCE = make_symbol('react.module.reference');


def is_react_component(component: JsProxy) -> bool:
    if callable(component):
        return True

    if component in [REACT_FRAGMENT_TYPE, REACT_PROFILER_TYPE, REACT_STRICT_MODE_TYPE, REACT_SUSPENSE_TYPE, 
                      REACT_SUSPENSE_LIST_TYPE, REACT_OFFSCREEN_TYPE]:
        return True
    
    component_meta = getattr(component, '$$typeof')
    if component_meta in [REACT_LAZY_TYPE,  REACT_MEMO_TYPE,  REACT_PROVIDER_TYPE,  
                           REACT_CONTEXT_TYPE,  REACT_FORWARD_REF_TYPE, REACT_MODULE_REFERENCE]:
        return True

    return hasattr(component, 'getModuleId')
