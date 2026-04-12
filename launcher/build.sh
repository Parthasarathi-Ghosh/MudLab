#!/bin/bash
export PATH=/mingw64/bin:$PATH
cd /c/GitHub/MudLab/launcher

# Compile the resource file (embeds the app icon into the .exe)
windres mudlab.rc -o mudlab_res.o && echo "mudlab_res.o compiled"

gcc -mconsole -O2 -o mudlab-cmd.exe mudlab_launcher.c mudlab_res.o && echo "mudlab-cmd.exe built"
gcc -mwindows -O2 -DGUI_MODE -o mudlab.exe mudlab_launcher.c mudlab_res.o && echo "mudlab.exe built"
