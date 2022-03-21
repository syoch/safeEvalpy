from .patcher import patcher

_open = open


def controller(code):
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
