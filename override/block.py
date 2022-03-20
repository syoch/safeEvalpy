from types import FunctionType


class BlockedException(Exception):
    def __init__(self, *args: object) -> None:
        raise Exception("blocked")


class Block(Exception):
    pass


def block(name: str = "") -> FunctionType:
    def wrap(*args, **kw):
        raise Block(f"{name} is blocked")
    return wrap
