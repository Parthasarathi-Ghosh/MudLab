#!/bin/bash
export PATH=/mingw64/bin:$PATH
cd /c/GitHub/MudLab/launcher

gcc -mconsole -O2 -o mudlab-cmd.exe mudlab_launcher.c && echo "mudlab-cmd.exe built"
gcc -mwindows -O2 -DGUI_MODE -o mudlab.exe mudlab_launcher.c && echo "mudlab.exe built"
