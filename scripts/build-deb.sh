#!/bin/bash

# Configuration
PKG_NAME="menu-logoff"
VERSION="1.0.0"
DEB_NAME="releases/${PKG_NAME}_${VERSION}_amd64.deb"
BUILD_DIR="deb-build"

echo "🚀 Starting Debian package creation for ZorinOS..."

# 1. Validation
if [ ! -f ".build/dist/main" ]; then
    echo "⚠️ ERROR: .build/dist/main not found. Please run PyInstaller first!"
    exit 1
fi

# 2. Cleanup and Folder Structure
echo "📁 Preparing directory structure..."
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR/usr/local/bin
mkdir -p $BUILD_DIR/usr/share/applications
mkdir -p $BUILD_DIR/usr/share/pixmaps
mkdir -p $BUILD_DIR/DEBIAN

# 3. Create Control File
echo "📝 Creating DEBIAN/control..."
cat <<EOF > $BUILD_DIR/DEBIAN/control
Package: $PKG_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Dyego Alves
Description: Custom power menu for Zorin OS with macOS-inspired aesthetics.
EOF

# 4. Create Desktop Entry
echo "🖥️ Creating Desktop entry..."
cat <<EOF > $BUILD_DIR/usr/share/applications/menu-logoff.desktop
[Desktop Entry]
Name=Menu Logoff
Comment=Custom logoff menu for Zorin
Exec=/usr/local/bin/menu-logoff
Icon=$PKG_NAME
Terminal=false
Type=Application
Categories=System;Utility;
Keywords=shutdown;reboot;logout;suspend;
StartupWMClass=menu-logoff
EOF

# 5. Copy Binary and Icon
echo "⚙️ Copying files..."
cp .build/dist/main $BUILD_DIR/usr/local/bin/menu-logoff
chmod +x $BUILD_DIR/usr/local/bin/menu-logoff

# Install icon in standard hicolor theme locations (multiple sizes)
# For now, use the 96x96 icon and copy to hicolor structure
ICON_SRC="app/assets/icons/icon-app.png"
mkdir -p $BUILD_DIR/usr/share/icons/hicolor/96x96/apps
cp $ICON_SRC $BUILD_DIR/usr/share/icons/hicolor/96x96/apps/$PKG_NAME.png

# Also keep in pixmaps for compatibility
cp $ICON_SRC $BUILD_DIR/usr/share/pixmaps/$PKG_NAME.png

# 6. Build the Deb
echo "📦 Building the package..."
dpkg-deb --build $BUILD_DIR $DEB_NAME

# 7. Final Cleanup
rm -rf $BUILD_DIR

echo "✅ SUCCESS! Package created: $DEB_NAME"
echo "👉 To install, run: make install-deb"
