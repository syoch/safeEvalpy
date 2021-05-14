import builtins
from . import config
import sys
import io
ctx = {
    "stdout": io.StringIO,
    "backup": {
        "stdout": sys.stdout
    }
}


def apply():
    # stream override
    buf = io.StringIO()
    bak_stdout = sys.stdout
    sys.stdout = buf
    # Function Override
    org = {}
    for funcname in config.blocks["builtinFuncs"]:
        org[funcname] = builtins[funcname]
        if config.blocks["builtinFuncs"][funcname]:
            builtins[funcname] = locals()[
                config.blocks["builtinFuncs"][funcname]
            ]
        else:
            builtins[funcname] = block(funcname+"()")
