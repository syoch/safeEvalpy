import builtins
from .core import ctx, restore,apply
from .config import blockedModules, blockedFunctions
from . import block
from . import config


def func(name, _globals=None, _locals=None, fromlist=(), level=0):
    basename = name.split(".")[0]
    if basename in blockedModules:
        raise block.Block(f"Module {basename} is blocked.")
    else:
        restore()
        obj = ctx["backup"]["__import__"](
            name, _globals, _locals, fromlist, level)
        apply()

    if basename in blockedFunctions:
        for funcnames in blockedFunctions[basename]:
            setattr(
                obj, funcnames,
                block.block(basename+"."+funcnames+"()")
            )
    if basename.replace("_", "") == "io":
        obj.open = open

        def open_code(path: str):
            if path.split("/")[-1] in config.blocks["file"]:
                raise Exception("can't open "+basename+".")
        obj.open_code = open_code

    return obj
