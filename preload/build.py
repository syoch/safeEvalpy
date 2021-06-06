#!/bin/python3
import os
workdir = os.path.dirname(__file__)
os.system(
    "gcc -shared -fPIC "
    f"{workdir}/preload.cpp "
    f"-o {workdir}/preload "
    "-ldl -rdynamic"
)
