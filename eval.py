import builtins
from typing import Any, Tuple
from .filter.listcomp import check as check_listcomp
from .exception_formatter import format as exception_format
import io
import os
import timeout_decorator

in_safeeval = False


@timeout_decorator.timeout(5)
def _eval(
    src: str, __globals={}, __locals={}
) -> Tuple[Any, str]:
    from . import override
    override.apply()
    override.context.stdout = io.StringIO()

    try:
        check_listcomp(src)

        __globals.update({"__builtins__": builtins})
        __locals.update({
            "buf": override.context.stdout,
            "__loader__": None,
            "__spec__": None
        })

        ret = eval(src, __globals, __locals)
    except BaseException as ex:
        try:
            ret = exception_format(ex)
        except BaseException:
            ret = "Exception: Unformattable exception"
    finally:
        if override.patches.enabled_patches:
            override.restore()

    stdout = override.context.stdout.getvalue()

    try:
        with open("safeEvalPy.log", "r") as fp:
            stdout += fp.read()
        os.remove("safeEvalPy.log")
    except Exception:
        pass

    return ret, stdout
