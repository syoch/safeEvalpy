def myRange(a=0, b=0, c=1):
    start = 0
    end = 0
    step = c

    if b == 0:  # argument count == 1
        end = a
    else:
        start = a
        end = b
    if end > 10**10:
        end = 100
    ret = org["range"](start, end, step)
    return ret


def myImport(name, _globals=None, _locals=None, fromlist=(), level=0):
    basename = name.split(".")[0]
    if basename in utilConf["module"]:
        raise Exception(f"Module {basename} is blocked.")
    else:
        obj = org["__import__"](
            name, _globals, _locals, fromlist, level)

    if basename in utilConf["funcs"]:
        for funcnames in utilConf["funcs"][basename]:
            setattr(obj, funcnames, block(
                basename+"."+funcnames+"()"))
    return obj


def block(name: str = ""):
    def wrap(*args):
        raise Exception(f"{name} is blocked")
    return wrap


def myOpen(path, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    basename = pathlib.Path(path).name
    if basename in utilConf["file"]:
        raise Exception("can't open "+basename+".")
    return org["open"](path, mode, buffering, encoding, errors, newline, closefd, opener)


def myPrint(*objects, sep=' ', end='\n', file=buf, flush=False):
    nonlocal buf
    org["print"](*objects, sep=sep, end=end, file=buf, flush=False)


def myIter(objects, sentinel=None):
    if type(objects) == type(lambda: 0):
        if objects() != sentinel:


raise Exception("iter attack has detected!")
return iter(objects, sentinel=sentinel)
