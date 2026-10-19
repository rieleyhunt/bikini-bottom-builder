#!/bin/sh
# Builds BikiniBottomBuilder-x86_64.AppImage for Linux.
# Needs: Go 1.22+, Python 3, npm, and network access the first time (to fetch appimagetool).
# Running it needs a Chromium based browser (Chrome, Chromium, Edge, Brave); zenity or kdialog
# gives a native Save dialog, otherwise exports are saved through the browser.
set -e
cd "$(dirname "$0")"
[ -f index.html ] || { (cd ../editor && { [ -d node_modules ] || npm install; }) && python3 ../editor/build.py; }

GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -trimpath -ldflags "-s -w" -o bikini-bottom-builder .

rm -rf AppDir && mkdir -p AppDir/usr/bin
mv bikini-bottom-builder AppDir/usr/bin/
cp app.png AppDir/bikini-bottom-builder.png
cat > AppDir/bikini-bottom-builder.desktop <<'DESKTOP'
[Desktop Entry]
Type=Application
Name=Bikini Bottom Builder
Comment=Level editor for SpongeBob SquarePants: Battle for Bikini Bottom (GBA)
Exec=bikini-bottom-builder
Icon=bikini-bottom-builder
Categories=Development;Game;
Terminal=false
DESKTOP
cat > AppDir/AppRun <<'APPRUN'
#!/bin/sh
HERE="$(dirname "$(readlink -f "$0")")"
exec "$HERE/usr/bin/bikini-bottom-builder" "$@"
APPRUN
chmod +x AppDir/AppRun

TOOL=${APPIMAGETOOL:-./appimagetool}
if [ ! -x "$TOOL" ]; then
  curl -fsSL -o appimagetool https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage
  chmod +x appimagetool
  TOOL=./appimagetool
fi
# --appimage-extract-and-run lets it work without FUSE (CI machines, containers)
ARCH=x86_64 "$TOOL" --appimage-extract-and-run AppDir BikiniBottomBuilder-x86_64.AppImage
rm -rf AppDir
echo built BikiniBottomBuilder-x86_64.AppImage
