from .context import function_backups
from . import patcher_factory

patcher = patcher_factory.Patcher()


def controller(code):
    func = None
    if "open" in function_backups:
        func = function_backups["open"]
    else:
        func = open

    try:
        func(code, "r")
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
