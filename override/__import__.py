from .core import ctx
from . import config
from . import block

blockedFunctions = {
    "sys": ["exit"],
    "os": ["system", "fork", "_exit", "popen", "abort", "chdir", "fchdir", "getcwd", "open", "fdopen", ],
    "_thread": ["exit", "exit_thread"],
    "time": ["sleep"],
    "io": ["open", "open_code", "FileIO"],
    "_io": ["open", "open_code", "FileIO"],
    "tokenize": ["open", "_builtin_open"]
}
blockedModules = [
    "subprocess",
    "ctypes",
    "pip",
    "importlib", "imp",
    "socket", "urllib", "http",
    "fileinput", "pathlib"
]


def func(name, _globals=None, _locals=None, fromlist=(), level=0):
    basename = name.split(".")[0]
    if basename in blockedModules:
        raise Exception(f"Module {basename} is blocked.")
    else:
        obj = ctx["backup"]["__import__"](
            name, _globals, _locals, fromlist, level)

    if basename in blockedFunctions:
        for funcnames in blockedFunctions[basename]:
            setattr(obj, funcnames, block.block(
                basename+"."+funcnames+"()"))
    return obj
