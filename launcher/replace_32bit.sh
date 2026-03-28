#!/bin/bash
BINDIR=/c/GitHub/MudLab/data/bin
for f in "$BINDIR"/*.dll; do
    name=$(basename "$f")
    arch=$(file "$f" | grep -o 'PE32[+]*')
    if [ "$arch" = "PE32" ]; then
        if [ -f "/mingw64/bin/$name" ]; then
            cp "/mingw64/bin/$name" "$BINDIR/$name"
            echo "replaced: $name"
        else
            echo "no 64-bit replacement found: $name"
        fi
    fi
done
