import os
import builtins
from types import CodeType
from . import config
from . import block
import importlib
import sys
import io

ctx = {}


def init_ctx():
    global ctx
    ctx = {
        "stdout": io.StringIO,
        "backup": {
            "stdout": sys.stdout
        },
        "function_backups": {},
        "overrides": {

        },
        "enabled": False
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


def print_(x):
    if ctx["enabled"]:
        ctx["backup"]["stdout"].write(str(x)+"\n")
    else:
        print(x)
    return x


def apply() -> None:
    if ctx == {}:
        init_ctx()

    print_(f"apply {ctx['enabled']=}")
    if ctx["enabled"]:
        raise Exception("already applied")

    init_ctx()

    ctx["enabled"] = True

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

    # Function Override
    for funcname in config.blocks["builtinFuncs"]:
        ctx["function_backups"][funcname] = getattr(builtins, funcname)
        setattr(
            builtins,
            funcname,
            ctx["overrides"][funcname] if funcname in ctx["overrides"]
            else block.block(funcname+"()")
        )

    ctx["backup"]["SystemExit"] = builtins.SystemExit
    builtins.SystemExit = block.BlockedException

    ctx["modules"] = sys.modules
    sys.modules = {}


def restore() -> None:
    print_(f"restore {ctx['enabled']=}")
    if not ctx["enabled"]:
        raise Exception("not applied")

    ctx["enabled"] = False

    sys.stdout = ctx["backup"]["stdout"]
    sys.modules = ctx["backup"]["modules"]
    sys.meta_path = ctx["backup"]["metapath"]

    controller("%fnb")
    controller("%bnf")

    # restore functions
    for funcname in config.blocks["builtinFuncs"]:
        setattr(builtins, funcname, ctx["function_backups"][funcname])

    # Restore SystemExit
    builtins.SystemExit = ctx["backup"]["SystemExit"]

    # Restore sys.module
    sys.modules = ctx["modules"]
