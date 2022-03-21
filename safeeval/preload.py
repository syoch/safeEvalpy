from .context import function_backups
from . import patcher_factory

patcher = patcher_factory.Patcher()

_open = open


def controller(code):
    func = None

    try:
        _open(code, "r")
    except Exception:
        pass

    return 0


@patcher.apply
def apply():
    controller("%bf .env")
    controller("%fb")

    return None


@patcher.restore
def restore(_):
    controller("%fnb")
    controller("%bnf")
