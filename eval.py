import builtins
from .override.core import apply, restore, ctx


def _eval(src):
    apply()
    # EXECUTING!!!
    try:
        # check (ListComp attack)
        ret = eval(
            src,
            {
                "__builtins__": builtins
            },
            {
                "buf": ctx["stdout"],
            }
        )
    except Exception as ex:
        error = str(ex)

    stdout = ctx["stdout"].getvalue()
    restore()
