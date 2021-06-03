import pathlib
from .core import ctx
import builtins
from .core import ctx, restore, apply
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


def func(objects, sentinel=None):
    if type(objects) == type(lambda: 0):
        if objects() != sentinel:
            raise Exception("iter attack has detected!")
    return ctx["backup"]["iter"](objects, sentinel=sentinel)


def func(*objects, sep=' ', end='\n', file=None, flush=False):
    ctx["backup"]["print"](*objects, sep=sep, end=end,
                           file=ctx["stdout"], flush=False)


def func(a=0, b=0, c=1):
    start = 0
    end = 0
    step = c

    if b == 0:  # argument count == 1
        end = a
    else:
        start = a
        end = b
    if end > 10**10:
        end = 100
    ret = ctx["backup"]["range"](start, end, step)
    return ret


def func(path, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    if "w" in mode:
        raise Exception("can't open file in write mode")

    basename = pathlib.Path(path).name
    if basename in config.blocks["file"]:
        raise Exception("can't open "+basename+".")
    return ctx["backup"]["open"](path, mode, buffering, encoding, errors, newline, closefd, opener)
