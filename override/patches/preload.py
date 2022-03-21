from . import context


def controller(code):
    func = None
    if "open" in context.function_backups:
        func = context.function_backups["open"]
    else:
        func = open

    try:
        func(code, "r")
    except Exception:
        pass

    return 0


def debug(x):
    controller(f"%dbg {str(x)}")


def apply():
    controller("%bf .env")
    controller("%fb")


def restore():
    controller("%fnb")
    controller("%bnf")
