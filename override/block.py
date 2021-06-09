from types import FunctionType
from . import exc_hook as hook


class Block(Exception):
    pass


def block(name: str = "") -> FunctionType:
    def wrap(*args, **kw):
        hook.myRaise(Block, Block(f"{name} is blocked"), None)
    return wrap
