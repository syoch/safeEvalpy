import io
import sys
from . import config
import builtins as __builtins__
from .override.core import apply, restore


def _eval(src):
    apply()
    # EXECUTING!!!
    try:
        # check (ListComp attack)
        ret = eval(
            src,
            {
                "__builtins__": __builtins__
            },
            {
                "buf": buf,
            }
        )
    except Exception as ex:
        error = str(ex)

    stdout = buf.getvalue()
    restore()
