from ..dynamic import patcher as dynamic
from ..preload.switcher import patcher as preload
from ..static.switcher import patcher as static
from .patcher import patcher


@patcher.apply
def apply():
    preload.do_apply()
    # static.do_apply()
    dynamic.do_apply()

    return None


@patcher.restore
def restore(_):
    preload.do_restore()
    # static.do_restore()
    dynamic.do_restore()
