
_p = print


def jailbreak(func):
    from .switcher.switcher import patcher

    def wrapped(*args, **kw):
        patcher.do_restore()
        ret = func(*args, **kw)
        patcher.do_apply()
        return ret

    return wrapped
