from . import config
from .. import block
import builtins
from .overrides import override_table
from ..jailBreak import jailbreak
from .patcher import patcher


@patcher.apply
def apply():
    table = {}
    for funcname in config.builtin_functions_overrides:
        table[funcname] = getattr(builtins, funcname)
        setattr(
            builtins,
            funcname,
            jailbreak(override_table[funcname]) if funcname in override_table
            else block.block(funcname+"()")
        )

    return table


@patcher.restore
def restore(table):
    for funcname in config.builtin_functions_overrides:
        setattr(builtins, funcname, table[funcname])

    import importlib
    for module_name in config.module_block:
        importlib.reload(table["__import__"](module_name))
