import builtins
from typing import Any, Tuple
import io
import os
import timeout_decorator

from .exception_formatter import format as exception_format

from .filtering import check as check_listcomp

from .switcher import switcher
from . import context


@timeout_decorator.timeout(5)
def _eval(
    src: str, as_str=True, __globals={}, __locals={}
) -> Tuple[Any, str]:
    context.stdout = io.StringIO()

    try:
        check_listcomp(src)

        __globals.update({"__builtins__": builtins})
        __locals.update({
            "buf": context.stdout,
            "__loader__": None,
            "__spec__": None,
            "__builtins__": None
        })

        with switcher.patcher:
            ret = eval(src, __globals, __locals)
    except BaseException as ex:
        with switcher.patcher:
            ret = exception_format(ex)

    stdout = context.stdout.getvalue()

    try:
        with open("safeEvalPy.log", "r") as fp:
            stdout += fp.read()
        os.remove("safeEvalPy.log")
    except Exception:
        pass

    with switcher.patcher:
        ret = str(ret)

    return ret, stdout
