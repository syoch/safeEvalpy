from . import eval

eval._eval("(lambda x:[x.append(0) for a in x])([0])")
