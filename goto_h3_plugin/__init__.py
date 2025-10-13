# __init__.py — QGIS plugin entry point
def classFactory(iface):  # QGIS looks for this
    from .goto_h3_plugin import GoToH3Plugin
    return GoToH3Plugin(iface)

