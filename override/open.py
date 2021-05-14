import pathlib


def myOpen(path, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    basename = pathlib.Path(path).name
    if basename in utilConf["file"]:
        raise Exception("can't open "+basename+".")
    return ctx["backup"]["open"](path, mode, buffering, encoding, errors, newline, closefd, opener)
