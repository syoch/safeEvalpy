from . import config
from .. import block
import builtins
from .overrides import override_table
from .patcher import patcher


@patcher.apply
def apply():
    table = {}
    for name in config.blocked_functions:
        table[name] = getattr(builtins, name)
        func = block.block(name+"()")
        setattr(builtins, name, func)

    for name in override_table:
        table[name] = getattr(builtins, name)
        func = override_table[name]
        setattr(builtins, name, func)

    return table


@patcher.restore
def restore(table):
    for name in table:
        setattr(builtins, name, table[name])
