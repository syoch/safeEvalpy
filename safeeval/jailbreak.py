
from contextlib import ContextDecorator
from .switcher.patcher import patcher
from . import log


class JailBreak(ContextDecorator):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def __enter__(self) -> None:
        log.begin_block("JailBreak", self.name)
        patcher.do_restore()

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        patcher.do_apply()
        log.end_block()
        return False
