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

    }
}


def override(func: function):
    def wrapped(*args):
        restore()
        func(*args)
        apply()

    ctx["overrides"][func.__name__] = wrapped

    return wrapped


def apply() -> None:
    # stream override
    buf = io.StringIO()
    ctx["stdout"] = buf
    ctx["backup"]["stdout"] = sys.stdout
    sys.stdout = buf

    # Load all override functions
    overrides = {}
    for funcname in config.blocks["builtinFuncs"]:
        mode = config.blocks["builtinFuncs"][funcname]
        if mode == "override":
            modname = __name__.replace(".core", "."+funcname)
            overrides[funcname] = importlib.import_module(modname).func

    # Function Override
    for funcname in config.blocks["builtinFuncs"]:
        ctx["backup"][funcname] = getattr(builtins, funcname)
        mode = config.blocks["builtinFuncs"][funcname]
        if mode == "override":
            modname = __name__.replace(".core", "."+funcname)
            setattr(builtins, funcname, overrides[funcname])
        elif mode == "block":
            setattr(builtins, funcname, block.block(funcname+"()"))


def restore() -> None:
    # restore functions
    for funcname in config.blocks["builtinFuncs"]:
        setattr(builtins, funcname, ctx["backup"][funcname])
    # restore stdout
    sys.stdout = ctx["backup"]["stdout"]
