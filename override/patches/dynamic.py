from . import context
from .. import config, block
import builtins
from .overrides import override_table


def apply():
    for funcname in config.blocks["builtinFuncs"]:
        context.function_backups[funcname] = getattr(builtins, funcname)
        setattr(
            builtins,
            funcname,
            override_table[funcname] if funcname in override_table
            else block.block(funcname+"()")
        )


def restore():
    for funcname in config.blocks["builtinFuncs"]:
        setattr(builtins, funcname, context.function_backups[funcname])

    import importlib
    for module_name in config.blockedFunctions:
        importlib.reload(context.function_backups["__import__"](module_name))
