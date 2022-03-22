
from .switcher.patcher import patcher
_p = print


def jailbreak(func):
    def wrapped(*args, **kw):
        _p("[*]", "Jailbreak", func.__name__)
        patcher.do_restore()
        ret = func(*args, **kw)
        patcher.do_apply()
        _p("[*]", "Jailbreak", func.__name__, "Done")
        return ret
    return wrapped
