import importlib
import os
from typing import Any, Tuple
from .filter.listcomp import check as check_listcomp
import timeout_decorator
import traceback
import pathlib
import io
import sys


@timeout_decorator.timeout(5)
def _eval(
    src: str, __globals=None, __locals=None
) -> Tuple[Any, str]:
    core = importlib.import_module(".override.core", __package__)

    if core.ctx["override_mod"] == None:
        core.ctx["override_mod"] = importlib.import_module(
            ".override.overrides", __package__
        )

    if not __globals:
        __globals = globals()
    if not __locals:
        __locals = locals()

    del __locals["core"]

    core.controller("%bf token")
    core.controller("%fb")

    # stream override
    buf = io.StringIO()
    core.ctx["stdout"] = buf
    core.ctx["backup"]["stdout"] = sys.stdout
    sys.stdout = buf

    core.apply()
    try:
        check_listcomp(src)

        ret = eval(src, __globals, __locals)
    except Exception as ex:
        ret = ""
        ret += 'Exception:\n'

        tb = ex.__traceback__
        while tb:
            fname = tb.tb_frame.f_code.co_filename
            if fname.startswith(os.getcwd()):
                fname = fname[len(os.getcwd())+1:]
            ret += '  in %s:%d (%s)\n' % (
                fname,
                tb.tb_lineno,
                tb.tb_frame.f_code.co_name
            )
            tb = tb.tb_next

        ret += f'  Detail: ({type(ex).__name__}) {ex}\n'

    sys.stdout = core.ctx["backup"]["stdout"]
    core.controller("%fnb")
    core.controller("%bnf")
    core.restore()

    stdout = core.ctx["stdout"].getvalue()

    # read preload log
    # importlib.reload(os)  # for use os.remove
    try:
        with open("safeEvalPy.log", "r") as fp:
            stdout += fp.read()
        os.remove("safeEvalPy.log")
    except Exception as ex:
        pass

    return ret, stdout
