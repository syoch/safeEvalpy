
import sys
import builtins
from .. import block
from . import context


def apply():
    global context

    context.backups["stdout"] = sys.stdout
    context.backups["modules"] = sys.modules
    context.backups["metapath"] = sys.meta_path
    context.backups["SystemExit"] = builtins.SystemExit

    sys.stdout = context.stdout
    sys.modules = {}
    sys.meta_path = []
    builtins.SystemExit = block.BlockedException


def restore():
    sys.stdout = context.backups["stdout"]
    sys.modules = context.backups["modules"]
    sys.meta_path = context.backups["metapath"]
    builtins.SystemExit = context.backups["SystemExit"]
