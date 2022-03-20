import os
import builtins
from types import CodeType
from . import config
from . import block
import importlib
import sys
import io


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


def restore() -> None:
    print_(f"restore {ctx['enabled']=}")
    if not ctx["enabled"]:
        raise Exception("not applied")

    ctx["enabled"] = False
