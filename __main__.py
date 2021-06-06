from . import eval

out, ret = eval._eval("__import__(\"os\").forkpty()")

print(out)
print(ret)
