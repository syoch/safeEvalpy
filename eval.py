from typing import Any, Tuple
from .override.core import apply, restore, ctx
from .filter.listcomp import check as check_listcomp
import timeout_decorator


@timeout_decorator.timeout(5)
def _eval(src: str, *args, **kwargs) -> Tuple[Any, str]:
    apply()
    try:
        # check ListComp Attack!
        check_listcomp(src)
        # EXECUTING!!!
        ret = eval(src, *args, **kwargs)
    except Exception as ex:
        ret = "Error:  "+type(ex).__name__+": "+str(ex)

    stdout = ctx["stdout"].getvalue()
    restore()

    return ret, stdout
