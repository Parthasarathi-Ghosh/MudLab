#!/bin/bash
export PATH=/mingw64/bin:$PATH
cd /c/GitHub/MudLab/launcher

gcc -mwindows -O2 -o mudlab.exe mudlab_launcher.c \
    -I/mingw64/include/python3.14 \
    -L/mingw64/lib \
    -lpython3.14 && echo "mudlab.exe built"

gcc -mconsole -O2 -o mudlab-cmd.exe mudlab_launcher.c \
    -I/mingw64/include/python3.14 \
    -L/mingw64/lib \
    -lpython3.14 && echo "mudlab-cmd.exe built"
