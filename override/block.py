def block(name: str = ""):
    def wrap(*args):
        raise Exception(f"{name} is blocked")
    return wrap
