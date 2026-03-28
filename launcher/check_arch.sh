#!/bin/bash
for f in /c/GitHub/MudLab/data/bin/*.dll; do
    arch=$(file "$f" | grep -o 'PE32[+]*')
    if [ "$arch" = "PE32" ]; then
        echo "32-bit: $(basename $f)"
    fi
done
