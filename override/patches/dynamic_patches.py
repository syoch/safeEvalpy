from . import context
from .. import config, block
import builtins


def apply_dynamic_patches():
    for funcname in config.blocks["builtinFuncs"]:
        context.function_backups[funcname] = getattr(builtins, funcname)
        setattr(
            builtins,
            funcname,
            context.overrides[funcname] if funcname in context.overrides
            else block.block(funcname+"()")
        )


def restore_dynamic_patches():
    for funcname in config.blocks["builtinFuncs"]:
        setattr(builtins, funcname, context.function_backups[funcname])
