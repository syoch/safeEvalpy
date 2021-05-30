from .core import ctx
from .config import blockedModules, blockedFunctions
from . import block


def func(name, _globals=None, _locals=None, fromlist=(), level=0):
    basename = name.split(".")[0]
    if basename in blockedModules:
        raise block.Block(f"Module {basename} is blocked.")
    else:
        obj = ctx["backup"]["__import__"](
            name, _globals, _locals, fromlist, level)

    if basename in blockedFunctions:
        for funcnames in blockedFunctions[basename]:
            setattr(
                obj, funcnames,
                block.block(basename+"."+funcnames+"()")
            )
    return obj
