import os
import builtins
from types import CodeType
from . import config
from . import block
import importlib
import sys
import io

ctx = {
    "stdout": io.StringIO,
    "backup": {
        "stdout": sys.stdout
    },
    "overrides": {

    },
    "override_mod": None
}


def controller(code):
    func = None
    if "__import__" in ctx["backup"]:
        importlib.reload(os)
        func = os.open
    else:
        func = os.open
    try:
        func(code, 0, 0)
    except Exception as ex:
        print(ex)
    return 0


def apply() -> None:
    controller("%fb")

    if ctx["override_mod"] == None:
        ctx["override_mod"] = importlib.import_module(
            ".overrides", __package__
        )

    # stream override
    buf = io.StringIO()
    ctx["stdout"] = buf
    ctx["backup"]["stdout"] = sys.stdout
    sys.stdout = buf

    # Function Override
    for funcname in config.blocks["builtinFuncs"]:
        ctx["backup"][funcname] = getattr(builtins, funcname)
        setattr(
            builtins,
            funcname,
            ctx["overrides"][funcname] if funcname in ctx["overrides"]
            else block.block(funcname+"()")
        )


def restore() -> None:
    # restore functions
    for funcname in config.blocks["builtinFuncs"]:
        setattr(builtins, funcname, ctx["backup"][funcname])
    # restore stdout
    sys.stdout = ctx["backup"]["stdout"]
    # restore fork
    controller("%fnb")
