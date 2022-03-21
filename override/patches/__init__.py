from . import dynamic
from . import preload
from . import static

enabled_patches = False


def apply():
    global enabled_patches

    if not enabled_patches:
        preload.apply()
        static.apply()
        dynamic.apply()

        enabled_patches = True


def restore():
    global enabled_patches

    if enabled_patches:
        static.restore()
        dynamic.restore()
        preload.restore()
        enabled_patches = False
