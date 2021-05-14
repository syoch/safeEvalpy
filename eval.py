import io
import sys
from . import config
import builtins as __builtins__


def _eval(src):
    # overriding stdout
    buf = io.StringIO()
    bak_stdout = sys.stdout
    sys.stdout = buf

    # override functions
    org = {}
    for funcname in config.blocks["builtinFuncs"]:
        org[funcname] = __builtins__[funcname]
        if config.blocks["builtinFuncs"][funcname]:
            __builtins__[funcname] = locals(
            )[config.blocks["builtinFuncs"][funcname]]
        else:
            __builtins__[funcname] = block(funcname+"()")

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
