from typing import Any


_print = print


def disabled_function(*a, **kw):
    raise Exception("Disabled function")


enabled_patches = []


class Patcher():
    def __init__(self):
        self.apply_function = None
        self.restore_function = None

        self.saved: Any = None
        self.patched: bool = False

    def apply(self, func):
        self.apply_function = func
        return disabled_function

    def restore(self, func):
        self.restore_function = func
        return disabled_function

    def do_apply(self):
        global enabled_patches

        _print("Applying", self.apply_function.__module__)

        if not self.apply_function:
            raise Exception("No apply function")

        if self.patched:
            raise Exception("Already patched")

        self.saved = self.apply_function()
        self.patched = True

        enabled_patches.append(self)

    def do_restore(self):
        _print("Restoring", self.restore_function.__module__)
        if not self.restore_function:
            raise Exception("No restore function")

        if not self.patched:
            raise Exception("Not patched")

        self.restore_function(self.saved)
        self.patched = False

        enabled_patches.remove(self)

    def __enter__(self):
        self.do_apply()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.do_restore()
        return False
