from typing import Any, Tuple
from .override.core import apply, restore, ctx
from .filter.listcomp import check as check_listcomp
import timeout_decorator
import traceback


@timeout_decorator.timeout(5)
def _eval(src: str) -> Tuple[Any, str]:
    apply()
    try:
        # check ListComp Attack!
        check_listcomp(src)
        # EXECUTING!!!
        ret = eval(src)
        restore()
    except Exception as ex:
        restore()
        ret = ''.join(traceback.TracebackException.from_exception(ex).format())

    stdout = ctx["stdout"].getvalue()

    return ret, stdout
