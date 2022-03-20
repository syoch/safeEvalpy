from . import dynamic_patches
from . import preload_patches
from . import static_patches

enabled_patches = False


def apply_patches():
    global enabled_patches

    if enabled_patches:
        raise Exception("already applied")

    preload_patches.apply()
    static_patches.apply()
    dynamic_patches.apply()

    enabled_patches = True


def restore_patches():
    global enabled_patches

    if not enabled_patches:
        raise Exception("not applied")

    dynamic_patches.restore()
    static_patches.restore()
    preload_patches.restore()

    enabled_patches = False
