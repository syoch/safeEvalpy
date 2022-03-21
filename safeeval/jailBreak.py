

def jailbreak(func):
    def wrapped(*args, **kw):
        from .switcher import patcher
        patcher.do_restore()
        ret = func(*args, **kw)
        patcher.do_apply()
        return ret

    return wrapped
