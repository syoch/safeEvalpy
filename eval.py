import builtins
from .override.core import apply, restore, ctx
from .filter.listcomp import check as check_listcomp


def _eval(src):
    # check ListComp Attack!
    check_listcomp(src)
    apply()
    # EXECUTING!!!
    try:
        # check (ListComp attack)
        ret = eval(src)
    except Exception as ex:
        error = str(ex)

    stdout = ctx["stdout"].getvalue()
    restore()
