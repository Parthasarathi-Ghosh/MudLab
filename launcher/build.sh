#!/bin/bash
export PATH=/mingw64/bin:$PATH
cd /c/GitHub/PyXRD.clays/launcher

gcc -mwindows -O2 -o pyxrd_clays.exe pyxrd_launcher.c \
    -I/mingw64/include/python3.14 \
    -L/mingw64/lib \
    -lpython3.14 && echo "pyxrd_clays.exe built"

gcc -mconsole -O2 -o pyxrd_clays-cmd.exe pyxrd_launcher.c \
    -I/mingw64/include/python3.14 \
    -L/mingw64/lib \
    -lpython3.14 && echo "pyxrd_clays-cmd.exe built"
