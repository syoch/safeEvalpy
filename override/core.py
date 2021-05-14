import builtins
from . import config
from . import block
import importlib
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
        mode = config.blocks["builtinFuncs"][funcname]
        if mode == "override":
            builtins[funcname] = importlib.import_module(funcname, ".").func
        elif mode == "block":
            builtins[funcname] = block.block(funcname+"()")


def restore():
    # restore functions
    for funcname in config.blocks["builtinFuncs"]:
        builtins[funcname] = ctx["backup"][funcname]
    # restore stdout
    sys.stdout = ctx["backup"]["stdout"]
