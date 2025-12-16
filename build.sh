#!/bin/bash
# Build script to create a distributable QGIS plugin with bundled dependencies

echo "Building GoToH3 QGIS Plugin..."

# Clean previous builds
rm -rf goto_h3_plugin/libs
rm -f goto_h3_plugin_*.zip

# Install h3 into libs directory
echo "Installing h3 dependency..."
pip install h3>=3.7.0 --target ./goto_h3_plugin/libs --upgrade

# Remove unnecessary files to reduce size
echo "Cleaning up unnecessary files..."
find goto_h3_plugin/libs -name "*.pyc" -delete
find goto_h3_plugin/libs -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find goto_h3_plugin/libs -name "*.dist-info" -type d -exec rm -rf {} + 2>/dev/null
find goto_h3_plugin/libs -name "tests" -type d -exec rm -rf {} + 2>/dev/null
find goto_h3_plugin/libs -name "test" -type d -exec rm -rf {} + 2>/dev/null

# Read version from metadata.txt
VERSION=$(grep "^version=" goto_h3_plugin/metadata.txt | cut -d'=' -f2)

# Create zip file
echo "Creating plugin zip file..."
zip -r "goto_h3_plugin_${VERSION}.zip" goto_h3_plugin/ -x "*.pyc" "*__pycache__*" "*.git*"

echo "Build complete: goto_h3_plugin_${VERSION}.zip"
echo "This zip file includes the h3 dependency and can be uploaded to the QGIS plugin repository."