import importlib
from . import exc_hook as hook


def jailbreak(func):
    core = importlib.import_module(".core", __package__)

    def wrapped(*args):
        core.restore()
        try:
            ret = func(*args)
        except Exception as ex:
            ret = None
            hook.myRaise(type(ex), ex, ex.__traceback__)
        core.apply()
        return ret

    return wrapped
