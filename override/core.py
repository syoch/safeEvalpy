import builtins
from . import config
from . import block
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
    ctx["backup"]["stdout"] = sys.stdout
    sys.stdout = buf
    # Function Override
    for funcname in config.blocks["builtinFuncs"]:
        ctx["backup"][funcname] = builtins[funcname]
        if config.blocks["builtinFuncs"][funcname]:
            builtins[funcname] = locals()[
                config.blocks["builtinFuncs"][funcname]
            ]
        else:
            builtins[funcname] = block.block(funcname+"()")


def restore():
    # restore functions
    for funcname in config.blocks["builtinFuncs"]:
        builtins[funcname] = ctx["backup"][funcname]
    # restore stdout
    sys.stdout = ctx["backup"]["stdout"]
