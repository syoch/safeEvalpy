import builtins
import importlib
import os
from typing import Any, Tuple
from .filter.listcomp import check as check_listcomp
import timeout_decorator
import io
import sys


@timeout_decorator.timeout(5)
def _eval(
    src: str, __globals=None, __locals=None
) -> Tuple[Any, str]:
    core = importlib.import_module(".override.core", __package__)

    if core.ctx["override_mod"] is None:
        core.ctx["override_mod"] = importlib.import_module(
            ".override.overrides", __package__
        )

    core.controller("%bf token")
    core.controller("%fb")

    # stream override
    buf = io.StringIO()
    core.ctx["stdout"] = buf
    core.ctx["backup"]["stdout"] = sys.stdout
    sys.stdout = buf

    core.ctx["backup"]["modules"] = sys.modules
    sys.modules = {}

    if not __globals:
        __globals = {
            "__builtins__": builtins
        }
    if not __locals:
        __locals = {
            "buf": buf,
            "__loader__": None,
            "__spec__": None
        }

    core.apply()
    try:
        check_listcomp(src)

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

    sys.stdout = core.ctx["backup"]["stdout"]
    sys.modules = core.ctx["backup"]["modules"]
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
    except Exception:
        pass

    return ret, stdout
