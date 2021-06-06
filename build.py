#!/bin/python3
import os
workdir = os.path.dirname(__file__)
os.system(
    f"gcc -shared -fPIC "
    f"{workdir}/preload.cpp "
    f"-o {workdir}/preload "
    f"-ldl -rdynamic"
)
