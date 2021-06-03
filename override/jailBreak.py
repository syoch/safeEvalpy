import importlib


def jailbreak(func):
    core = importlib.import_module(".core", __package__)

    def wrapped(*args):
        core.restore()
        ret = func(*args)
        core.apply()
        return ret

    return wrapped
