import builtins
import importlib
import os
from typing import Any, Tuple
from .filter.listcomp import check as check_listcomp
import timeout_decorator
import io
import sys


# @timeout_decorator.timeout(5)
def _eval(
    src: str, __globals={}, __locals={}
) -> Tuple[Any, str]:
    core = importlib.import_module(".override.core", __package__)

    core.apply()
    try:
        check_listcomp(src)

        __globals.update({"__builtins__": builtins})
        __locals.update({
            "buf": core.ctx["stdout"],
            "__loader__": None,
            "__spec__": None
        })

        ret = eval(src, __globals, __locals)
    except BaseException as ex:
        ret = ""
        ret += 'Exception:\n'

        tb = ex.__traceback__
        while tb:
            ret += '  in %s:%d (%s)\n' % (
                tb.tb_frame.f_code.co_filename.replace(os.getcwd(), "."),
                tb.tb_lineno,
                tb.tb_frame.f_code.co_name
            )
            tb = tb.tb_next

        ret += f'  Detail: ({type(ex).__name__}) {ex}\n'

    core.restore()

    stdout = core.ctx["stdout"].getvalue()

    # read preload log
    # importlib.reload(os)  # for use os.remove
    try:
        with open("safeEvalPy.log", "r") as fp:
            stdout += fp.read()
        os.remove("safeEvalPy.log")
    except Exception:
        pass

    return ret, stdout
