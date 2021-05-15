from . import config
import builtins
from .override.core import apply, restore


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
                "buf": buf,
            }
        )
    except Exception as ex:
        error = str(ex)

    stdout = buf.getvalue()
    restore()
