from .core import ctx


def myPrint(*objects, sep=' ', end='\n', file=None, flush=False):
    ctx["backup"]["print"](*objects, sep=sep, end=end,
                           file=ctx["backup"]["stdout"], flush=False)
