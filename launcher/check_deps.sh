#!/bin/bash
BINDIR=/c/GitHub/MudLab/data/bin
MISSING=()

check_dll() {
    local dll="$1"
    local deps
    deps=$(objdump -p "$BINDIR/$dll" 2>/dev/null | grep 'DLL Name' | awk '{print $3}')
    for dep in $deps; do
        # Skip Windows system DLLs
        case "${dep,,}" in
            kernel32.dll|user32.dll|gdi32.dll|msvcrt.dll|advapi32.dll|ole32.dll|shell32.dll|\
            ws2_32.dll|ntdll.dll|comctl32.dll|rpcrt4.dll|shlwapi.dll|dwrite.dll|usp10.dll|\
            opengl32.dll|psapi.dll|secur32.dll|iphlpapi.dll|winspool.drv|comdlg32.dll|\
            imm32.dll|winmm.dll|crypt32.dll|version.dll|cfgmgr32.dll|d3d11.dll|dxgi.dll)
                continue ;;
        esac
        if [ ! -f "$BINDIR/$dep" ]; then
            echo "MISSING: $dep (needed by $dll)"
            if [ -f "/mingw64/bin/$dep" ]; then
                cp "/mingw64/bin/$dep" "$BINDIR/" && echo "  -> copied from MSYS2"
            else
                echo "  -> NOT IN MSYS2 either!"
            fi
        fi
    done
}

for dll in "$BINDIR"/*.dll; do
    check_dll "$(basename $dll)"
done
