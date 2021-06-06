#!/bin/bash
gcc -shared -fPIC preload.cpp -ldl -o preload -rdynamic
