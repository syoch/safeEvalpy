from . import config
from .. import block
import builtins
from .overrides import override_table
from ..jailbreak import JailBreak
from .patcher import patcher


@patcher.apply
def apply():
    table = {}
    for funcname in config.builtin_functions_overrides:
        table[funcname] = getattr(builtins, funcname)

        if funcname in override_table:
            func = JailBreak(funcname)(override_table[funcname])
        else:
            func = block.block(funcname+"()")

        setattr(builtins, funcname, func)

    return table


@patcher.restore
def restore(table):
    for funcname in config.builtin_functions_overrides:
        setattr(builtins, funcname, table[funcname])
