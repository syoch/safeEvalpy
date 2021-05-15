from types import FunctionType


def block(name: str = "") -> FunctionType:
    def wrap(*args):
        raise Exception(f"{name} is blocked")
    return wrap
