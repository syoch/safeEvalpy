def myIter(objects, sentinel=None):
    if type(objects) == type(lambda: 0):
        if objects() != sentinel:
            raise Exception("iter attack has detected!")
    return ctx["backup"]["iter"](objects, sentinel=sentinel)
