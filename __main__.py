from . import eval

out, ret = eval._eval("__import__(\"ctypes\")")

print(ret)
print(out)
