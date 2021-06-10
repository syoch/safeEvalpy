import importlib


def jailbreak(func):
    core = importlib.import_module(".core", __package__)

    def wrapped(*args, **kw):
        core.restore()
        ret = func(*args, **kw)
        core.apply()
        return ret

    return wrapped
