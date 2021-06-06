from . import eval

out, ret, log = eval._eval("__import__(\"ctypes\")")

print(ret)
print(out+log)
