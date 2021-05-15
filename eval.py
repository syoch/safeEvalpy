import builtins
from .override.core import apply, restore, ctx
from .filter.listcomp import check as check_listcomp


def _eval(src: str):
    apply()
    try:
        # check ListComp Attack!
        check_listcomp(src)
        # EXECUTING!!!
        ret = eval(src)
    except Exception as ex:
        ret = "Error:  "+type(ex).__name__+": "+str(ex)

    stdout = ctx["stdout"].getvalue()
    restore()

    return ret, stdout
