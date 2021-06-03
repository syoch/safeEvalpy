import pathlib
from .core import ctx, restore, apply
import builtins
from .config import blockedModules, blockedFunctions
from . import block
from . import config


def override(func):
    def wrapped(*args):
        restore()
        func(*args)
        apply()

    realname = func.__name__
    if realname[0:8] == "__wrap__":
        realname = realname[8:]

    ctx["overrides"][realname] = wrapped

    return wrapped


@override
def __wrap____import__(name, *args):
    basename = name.split(".")[0]
    if basename in blockedModules:
        raise block.Block(f"Module {basename} is blocked.")
    else:
        obj = __import__(name, *args)

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


@override
def __wrap__iter(objects, sentinel=None):
    if type(objects) == type(lambda: 0):
        if objects() != sentinel:
            raise Exception("iter attack has detected!")
    return iter(objects, sentinel=sentinel)


@override
def __wrap__print(*objects, sep=' ', end='\n', file=None, flush=False):
    print(*objects, sep=sep, end=end,
          file=file, flush=False)


@override
def __wrap__range(a=0, b=0, c=1):
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
    ret = range(start, end, step)
    return ret


@override
def __wrap__open(path, mode='r', *args):
    if "w" in mode:
        raise Exception("can't open file in write mode")

    basename = pathlib.Path(path).name
    if basename in config.blocks["file"]:
        raise Exception("can't open "+basename+".")

    return open(path, mode, *args)
