
from .switcher.patcher import patcher


def jailbreak(func):
    def wrapped(*args, **kw):
        patcher.do_restore()
        ret = func(*args, **kw)
        patcher.do_apply()
        return ret
    return wrapped
