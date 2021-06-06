#!/bin/bash
cd `dirname $0`
gcc -shared -fPIC preload.cpp -ldl -o preload -rdynamic
