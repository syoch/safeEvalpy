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