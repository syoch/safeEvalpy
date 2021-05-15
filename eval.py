import builtins
from .override.core import apply, restore, ctx
from .filter.listcomp import check as check_listcomp


def _eval(src):
    apply()
    try:
        # check ListComp Attack!
        check_listcomp(src)
        # EXECUTING!!!
        ret = eval(src)
    except Exception as ex:
        error = str(ex)

    stdout = ctx["stdout"].getvalue()
    restore()
