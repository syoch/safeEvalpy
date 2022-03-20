from . import patches

import importlib


def jailbreak(func):
    def wrapped(*args, **kw):
        patches.restore()
        ret = func(*args, **kw)
        patches.apply()
        return ret

    return wrapped
