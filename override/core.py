import builtins
from . import config


def apply():
    # stream override
    buf = io.StringIO()
    bak_stdout = sys.stdout
    sys.stdout = buf
    # Function Override
    org = {}
    for funcname in config.blocks["builtinFuncs"]:
        org[funcname] = builtins[funcname]
        if config.blocks["builtinFuncs"][funcname]:
            builtins[funcname] = locals()[
                config.blocks["builtinFuncs"][funcname]
            ]
        else:
            builtins[funcname] = block(funcname+"()")
