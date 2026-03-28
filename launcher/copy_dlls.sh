#!/bin/bash
DLLS="libavif-16.dll libimagequant.dll libjpeg-8.dll liblcms2-2.dll libopenjp2-7.dll libqhull_r.dll libraqm-0.dll libtiff-6.dll libwebp-7.dll libwebpdemux-2.dll libwebpmux-3.dll libgirepository-2.0-0.dll libxml2-16.dll"
DEST=/c/GitHub/MudLab/data/bin
for dll in $DLLS; do
  if [ -f /mingw64/bin/$dll ]; then
    cp /mingw64/bin/$dll $DEST/ && echo "copied $dll"
  else
    echo "NOT FOUND: $dll"
  fi
done
