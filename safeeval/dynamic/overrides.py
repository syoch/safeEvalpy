import pathlib

from .. import block
from . import config
from .. import context
from . import default_function

override_table = {}


def override(func):
    funcname = func.__name__

    if not funcname.startswith("wrap_"):
        raise Exception("override() must be used on wrap_* functions")

    funcname = funcname[5:]

    override_table[funcname] = func


@override
def wrap___import__(name, *args, **kwargs):
    basename = name.split(".")[0]
    if basename.startswith(".") or basename.startswith("libs"):
        raise block.Block("relative import is blocked.")

    if "eval" in name:
        raise block.Block("the module name which contains eval is blocked.")

    if basename in config.module_block and config.module_block[basename][0] == ...:
        raise block.Block(f"Module {basename} is blocked.")
    else:
        obj = default_function.get_default_function(
            "__import__")(name, *args, **kwargs)

    if basename in config.module_block:
        for funcnames in config.module_block[basename]:
            setattr(
                obj, funcnames,
                block.block(basename+"."+funcnames+"()")
            )

    if basename.replace("_", "") == "io":
        obj.open = override_table["open"]

        def open_code(path: str):
            if path.split("/")[-1] in config.blocks["file"]:
                raise Exception("can't open "+basename+".")
        obj.open_code = open_code

    if hasattr(obj, "__loader__"):
        del obj.__loader__

    if hasattr(obj, "__spec__"):
        del obj.__spec__

    return obj


@override
def wrap_iter(objects, sentinel=None):
    if type(objects) == type(lambda: 0):
        if objects() != sentinel:
            raise Exception("iter attack has detected!")

    return default_function.get_default_function("iter")(objects, sentinel=sentinel)


@override
def wrap_print(*objects, sep=' ', end='\n', file=None, flush=False):
    default_function.get_default_function("print")(*objects, sep=sep, end=end,
                                                   file=context.stdout, flush=False)


@override
def wrap_range(a=0, b=0, c=1):
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
    ret = default_function.get_default_function("range")(start, end, step)
    return ret


@override
def wrap_open(path, mode='r', *args):
    if "w" in mode or "a" in mode or "x" in mode:
        raise Exception("can't open file in write mode")

    basename = pathlib.Path(path).name
    if basename in config.blocked_files:
        raise Exception(f"can't open {basename} in protected mode.")

    if path[0] == "%":
        raise Exception("preload control is blocked.")

    return default_function.get_default_function("open")(path, mode, *args)
