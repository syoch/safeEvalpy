import io


indent = 0
do_logging = False

_p = print


def format(*args, **kwargs):
    buf = io.StringIO()
    _p(*args, **kwargs, file=buf, end="")
    return buf.getvalue()


def log(*args, **kwargs):
    global indent

    if not do_logging:
        return

    _p("| "*indent+format(*args, **kwargs))


def begin_block(*args, **kwargs):
    global indent
    log("-", *args, **kwargs)
    indent += 1


def end_block():
    global indent
    indent -= 1
    log("\\")


class Block:
    def __init__(self, *msg):
        self.msg = format(*msg)

    def __enter__(self):
        begin_block(self.msg)

    def __exit__(self, *args):
        end_block()
        return False


def set_do_logging(f: bool) -> None:
    global do_logging
    do_logging = f
