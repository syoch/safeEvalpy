import importlib
import os
from typing import Any, Tuple
from .filter.listcomp import check as check_listcomp
import timeout_decorator
import traceback


@timeout_decorator.timeout(5)
def _eval(
    src: str, __globals=None, __locals=None
) -> Tuple[Any, str]:
    core = importlib.import_module(".override.core", __package__)

    if not __globals:
        __globals = globals()
    if not __locals:
        __locals = locals()

    del __locals["core"]
    core.apply()
    try:
        # check ListComp Attack!
        check_listcomp(src)
        # EXECUTING!!!
        ret = eval(src, __globals, __locals)
        core.restore()
    except Exception as ex:
        core.restore()
        ret = ''.join(traceback.TracebackException.from_exception(ex).format())

    stdout = core.ctx["stdout"].getvalue()

    # read preload log
    try:
        with open("safeEvalPy.log", "r") as fp:
            log = fp.read()
        os.remove("safeEvalPy.log")
    except Exception as ex:
        log = ""
        pass

    return ret, stdout, log
