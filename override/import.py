from .core import ctx
from . import config
from . import block


def func(name, _globals=None, _locals=None, fromlist=(), level=0):
    basename = name.split(".")[0]
    if basename in config.blocks["module"]:
        raise Exception(f"Module {basename} is blocked.")
    else:
        obj = ctx["backup"]["__import__"](
            name, _globals, _locals, fromlist, level)

    if basename in config.blocks["funcs"]:
        for funcnames in config.blocks["funcs"][basename]:
            setattr(obj, funcnames, block.block(
                basename+"."+funcnames+"()"))
    return obj
