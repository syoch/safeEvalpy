
import sys
import builtins
from . import block
from . import patcher_factory
from . import context

patcher = patcher_factory.Patcher()


@patcher.apply
def apply():
    backup = [
        sys.stdout, sys.modules, sys.meta_path, builtins.SystemExit
    ]

    sys.stdout = context.stdout
    sys.modules = {}
    sys.meta_path = []
    builtins.SystemExit = block.BlockedException

    return backup


@patcher.restore
def restore(backup):
    (sys.stdout, sys.modules, sys.meta_path, builtins.SystemExit) = backup
