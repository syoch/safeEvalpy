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

    # restore functions
    for funcname in config.blocks["builtinFuncs"]:
        __builtins__[funcname] = org[funcname]
    # restore stdout
    sys.stdout = bak_stdout
    # get value
    stdout = buf.getvalue()
