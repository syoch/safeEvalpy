from .core import ctx


def func(*objects, sep=' ', end='\n', file=None, flush=False):
    ctx["backup"]["print"](*objects, sep=sep, end=end,
                           file=ctx["stdout"], flush=False)
