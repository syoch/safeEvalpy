from typing import Any, Tuple
from .override.core import apply, restore, ctx
from .filter.listcomp import check as check_listcomp
import timeout_decorator
import traceback


@timeout_decorator.timeout(5)
def _eval(
    src: str, __globals=None, __locals=None
) -> Tuple[Any, str]:

    if not __globals:
        __globals = globals()
    if not __locals:
        __locals = locals()

    apply()
    try:
        # check ListComp Attack!
        check_listcomp(src)
        # EXECUTING!!!
        ret = eval(src, __globals, __locals)
        restore()
    except Exception as ex:
        restore()
        ret = ''.join(traceback.TracebackException.from_exception(ex).format())

    stdout = ctx["stdout"].getvalue()

    return ret, stdout
