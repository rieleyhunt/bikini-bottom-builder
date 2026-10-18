#!/bin/sh
# Builds BikiniBottomBuilder.exe (cross-compiles from Linux/macOS/WSL).
# Needs: Go 1.22+, mingw-w64 (x86_64-w64-mingw32-windres), Python 3, npm.
set -e
cd "$(dirname "$0")"
(cd ../editor && { [ -d node_modules ] || npm install; }) && python3 ../editor/build.py
x86_64-w64-mingw32-windres --preprocessor=cpp -O coff -o rsrc_windows_amd64.syso app.rc
GOOS=windows GOARCH=amd64 CGO_ENABLED=0 go build -trimpath -ldflags "-H windowsgui -s -w" -o BikiniBottomBuilder.exe .
echo built BikiniBottomBuilder.exe
