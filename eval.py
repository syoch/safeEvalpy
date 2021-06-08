import importlib
import os
from typing import Any, Tuple
from .filter.listcomp import check as check_listcomp
import timeout_decorator
import traceback
import copy


@timeout_decorator.timeout(5)
def _eval(
    src: str, __globals=None, __locals=None
) -> Tuple[Any, str]:
    core = importlib.import_module(".override.core", __package__)
    core.controller("%bf token")
    core.controller("%fb")

    if not __globals:
        __globals = globals()
    if not __locals:
        __locals = locals()

    del __locals["core"]

    core.apply()
    try:
        check_listcomp(src)

        ret = eval(src, __globals, __locals)
    except Exception as ex:
        ret = ''.join(traceback.TracebackException.from_exception(ex).format())
    core.restore()

    stdout = core.ctx["stdout"].getvalue()

    # read preload log
    importlib.reload(os)  # for use os.remove
    try:
        with open("safeEvalPy.log", "r") as fp:
            stdout += fp.read()
        os.remove("safeEvalPy.log")
    except Exception as ex:
        print(ex)
        pass

    core.controller("%fnb")
    core.controller("%bnf")
    return ret, stdout
