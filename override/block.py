from types import FunctionType


class Block(Exception):
    pass


def block(name: str = "") -> FunctionType:
    def wrap(*args, **kw):
        raise Block(f"{name} is blocked")
    return wrap
