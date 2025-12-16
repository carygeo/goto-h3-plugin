# __init__.py — QGIS plugin entry point
import sys
import os

# Add the libs directory to Python path for bundled dependencies
plugin_dir = os.path.dirname(__file__)
libs_path = os.path.join(plugin_dir, 'libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

def classFactory(iface):  # QGIS looks for this
    from .goto_h3_plugin import GoToH3Plugin
    return GoToH3Plugin(iface)

