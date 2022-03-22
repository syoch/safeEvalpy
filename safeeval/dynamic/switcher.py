from . import config
from .. import block
import builtins
from .overrides import override_table
from ..jailBreak import jailbreak
from .patcher import patcher

_p = print


@patcher.apply
def apply():
    table = {}
    for funcname in config.builtin_functions_overrides:
        # _p("Overriding", funcname, "1")
        table[funcname] = getattr(builtins, funcname)

        if funcname in override_table:
            # _p("Overriding", funcname, "2 A")
            func = jailbreak(override_table[funcname])
        else:
            # _p("Overriding", funcname, "2 B")
            func = block.block(funcname+"()")

        # _p("Overriding", funcname, "3")
        setattr(builtins, funcname, func)

        # _p("Overriding", funcname, "-")

    return table


@patcher.restore
def restore(table):
    for funcname in config.builtin_functions_overrides:
        setattr(builtins, funcname, table[funcname])

    import importlib
    for module_name in config.module_block:
        importlib.reload(table["__import__"](module_name))
