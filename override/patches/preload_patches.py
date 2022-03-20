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


def apply_static_patches():
    controller("%bf token")
    controller("%fb")


def restore_static_patches():
    controller("%fnb")
    controller("%bnf")
