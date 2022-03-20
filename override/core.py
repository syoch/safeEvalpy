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
    if "open" in ctx["backup"]:
        func = ctx["backup"]["open"]
    else:
        func = open

    try:
        func(code, "r")
    except Exception as ex:
        pass

    return 0


class BlockedException(Exception):
    def __init__(self, *args: object) -> None:
        raise Exception("blocked")


def apply() -> None:
    controller("%bf token")
    controller("%fb")

    # stream override
    buf = io.StringIO()
    ctx["stdout"] = buf
    ctx["backup"]["stdout"] = sys.stdout
    sys.stdout = buf

    ctx["backup"]["modules"] = sys.modules
    sys.modules = {}

    ctx["backup"]["metapath"] = sys.meta_path
    sys.meta_path = []

    if ctx["override_mod"] == None:
        ctx["override_mod"] = importlib.import_module(
            ".overrides", __package__
        )

    # Function Override
    for funcname in config.blocks["builtinFuncs"]:
        ctx["backup"][funcname] = getattr(builtins, funcname)
        setattr(
            builtins,
            funcname,
            ctx["overrides"][funcname] if funcname in ctx["overrides"]
            else block.block(funcname+"()")
        )

    builtins.SystemExit = BlockedException

    ctx["modules"] = sys.modules
    sys.modules = {}


def restore() -> None:
    sys.stdout = ctx["backup"]["stdout"]
    sys.modules = ctx["backup"]["modules"]
    sys.meta_path = ctx["backup"]["metapath"]

    controller("%fnb")
    controller("%bnf")

    # restore functions
    for funcname in config.blocks["builtinFuncs"]:
        setattr(builtins, funcname, ctx["backup"][funcname])

    # Restore sys.module
    sys.modules = ctx["modules"]
