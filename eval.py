import io
import sys
from . import config
import builtins as __builtins__


def _eval(src):
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
