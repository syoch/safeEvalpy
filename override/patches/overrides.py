import importlib
import pathlib

from anyio import fail_after
from ..config import blockedModules, blockedFunctions
from .. import block
from .. import config
from ..jailBreak import jailbreak

override_table = {}


def override(original):
    funcname = original.__name__

    def coro(func):
        override_table[funcname] = func

        def wrap(*args, **kw):
            return func(original, *args, **kw)

        return wrap
    return coro


@override(__import__)
@jailbreak
def __import__(original, name, *args, **kwargs):
    basename = name.split(".")[0]
    if basename.startswith("."):
        raise block.Block("relative import is blocked.")

    if basename in blockedModules:
        raise block.Block(f"Module {basename} is blocked.")
    else:
        obj = original(name, *args, **kwargs)

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

    if hasattr(obj, "__loader__"):
        del obj.__loader__

    if hasattr(obj, "__spec__"):
        del obj.__spec__

    return obj


@override(iter)
def iter(original, objects, sentinel=None):
    if type(objects) == type(lambda: 0):
        if objects() != sentinel:
            raise Exception("iter attack has detected!")
    return original(objects, sentinel=sentinel)


@override(print)
def print(original, *objects, sep=' ', end='\n', file=None, flush=False):
    original(*objects, sep=sep, end=end,
             file=file, flush=False)


@override(range)
def range(original, a=0, b=0, c=1):
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
    ret = original(start, end, step)
    return ret


@override(open)
def open(original, path, mode='r', *args):
    if "w" in mode or "a" in mode or "x" in mode:
        raise Exception("can't open file in write mode")

    basename = pathlib.Path(path).name
    if basename in config.blocks["file"]:
        raise Exception("can't open "+basename+".")

    if path[0] == "%":
        raise Exception("preload control is blocked.")

    return original(path, mode, *args)
