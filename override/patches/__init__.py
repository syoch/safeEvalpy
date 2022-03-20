from . import dynamic_patches
from . import preload_patches
from . import static_patches


def apply_patches():
    preload_patches.apply()
    static_patches.apply()
    dynamic_patches.apply()


def restore_patches():
    dynamic_patches.restore()
    static_patches.restore()
    preload_patches.restore()
