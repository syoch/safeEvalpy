def myPrint(*objects, sep=' ', end='\n', file=buf, flush=False):
    nonlocal buf
    org["print"](*objects, sep=sep, end=end, file=buf, flush=False)
