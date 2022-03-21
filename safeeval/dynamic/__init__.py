from . import config
from .. import block, context
import builtins
from .overrides import override_table
from ..patcher_factory import Patcher


patcher = Patcher()


@patcher.apply
def apply():
    table = {}
    for funcname in config.builtin_functions_overrides:
        table[funcname] = getattr(builtins, funcname)
        setattr(
            builtins,
            funcname,
            override_table[funcname] if funcname in override_table
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
