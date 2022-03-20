from . import context


def controller(code):
    func = None
    if "open" in context.function_backups:
        func = context.function_backups["open"]
    else:
        func = open

    try:
        func(code, "r")
    except Exception as ex:
        pass

    return 0


def apply():
    controller("%bf token")
    controller("%fb")


def restore():
    controller("%fnb")
    controller("%bnf")
