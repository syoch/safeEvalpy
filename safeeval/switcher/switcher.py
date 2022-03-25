from ..dynamic.switcher import patcher as dynamic
from ..preload.switcher import patcher as preload
from ..static.switcher import patcher as static
from .patcher import patcher

from .. import log


@patcher.apply
def apply():
    # begin_block("Safeeval", "All")

    with log.Block("Safeeval", "All", "Apply"):
        preload.do_apply()
        static.do_apply()
        log.log("Applying dynamic patch")
        dynamic.do_apply()
    return None


@patcher.restore
def restore(_):
    with log.Block("Safeeval", "All", "Restore"):
        preload.do_restore()
        static.do_restore()
        log.log("Restoreing dynamic patch")
        dynamic.do_restore()

    # end_block()
