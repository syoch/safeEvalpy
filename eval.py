buf = io.StringIO()
bak_stdout = sys.stdout
sys.stdout = buf
org = {}
for funcname in utilConf["builtinFuncs"]:
    org[funcname] = __builtins__[funcname]
    if utilConf["builtinFuncs"][funcname]:
        __builtins__[funcname] = locals()[utilConf["builtinFuncs"][funcname]]
    else:
        __builtins__[funcname] = block(funcname+"()")
try:
    # check (ListComp attack)
    ret = eval(
        src,
        {
            "__builtins__": __builtins__
        },
        {
            "buf": buf,
        }
    )
except Exception as ex:
    error = str(ex)
for funcname in utilConf["builtinFuncs"]:
    __builtins__[funcname] = org[funcname]
sys.stdout = bak_stdout
stdout = buf.getvalue()
