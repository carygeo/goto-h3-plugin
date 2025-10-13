# goto_h3_plugin.py
# QGIS toolbar button: prompt for an H3 index, draw the cell (EPSG:4326), zoom in project CRS.

import os
import h3
from qgis.PyQt.QtCore import QObject, QVariant
from qgis.PyQt.QtWidgets import QAction, QInputDialog, QMessageBox
from qgis.PyQt.QtGui import QIcon
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsField,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsFillSymbol,
    QgsSingleSymbolRenderer,
    QgsCoordinateTransform,
)

class GoToH3Plugin(QObject):
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.action = None

    def initGui(self):
        # Action (toolbar + Plugins menu)
        self.action = QAction("Go To H3 Cell", self.iface.mainWindow())

        # Optional icon if icon.png exists in plugin folder
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            self.action.setIcon(QIcon(icon_path))

        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&H3 Tools", self.action)

    def _h3_resolution(self, h):
        """Return H3 resolution for both h3 v4 and v3 APIs."""
        try:
            # h3 v4
            return h3.get_resolution(h)
        except AttributeError:
            # h3 v3
            return h3.h3_get_resolution(h)

    def unload(self):
        if self.action:
            self.iface.removeToolBarIcon(self.action)
            self.iface.removePluginMenu("&H3 Tools", self.action)

    def run(self):
        # Prompt for one-or-many H3 indexes
        raw, ok = QInputDialog.getMultiLineText(
            self.iface.mainWindow(),
            "Go To H3 Cell(s)",
            "Paste one or more H3 indexes (comma, space, or newline-separated):",
        )
        if not ok:
            return

        import re
        items = [s.strip() for s in re.split(r"[,\s]+", raw.strip()) if s.strip()]
        if not items:
            return

        # Prepare a single memory layer in WGS84
        layer_name = f"H3 ({len(items)})"
        vl = QgsVectorLayer("Polygon?crs=EPSG:4326", layer_name, "memory")
        pr = vl.dataProvider()
        pr.addAttributes([
            QgsField("h3", QVariant.String),
            QgsField("res", QVariant.Int),   # <-- resolution column
        ])
        vl.updateFields()

        def boundary_for(h):
            # h3 v4 first, fallback to v3
            try:
                try:
                    b = h3.cell_to_boundary(h)  # v4 -> [(lat, lon), ...]
                except TypeError:
                    b = h3.h3_to_geo_boundary(h, geo_json=False)  # v3
                if not b or len(b) < 6:
                    raise ValueError("Invalid boundary")
                ring_xy = [QgsPointXY(lon, lat) for (lat, lon) in b]
                if ring_xy[0] != ring_xy[-1]:
                    ring_xy.append(ring_xy[0])
                return ring_xy
            except Exception:
                return None

        bad = []
        feats = []
        for h in items:
            ring_xy = boundary_for(h)
            if ring_xy is None:
                bad.append(h)
                continue

            # Compute resolution safely across h3 versions
            try:
                res_val = self._h3_resolution(h)
            except Exception:
                res_val = None

            feat = QgsFeature(vl.fields())
            feat.setGeometry(QgsGeometry.fromPolygonXY([ring_xy]))
            feat["h3"] = h
            if res_val is not None:
                feat["res"] = int(res_val)
            feats.append(feat)

        if not feats:
            QMessageBox.critical(self.iface.mainWindow(), "H3 Error",
                                 "No valid H3 indexes were found.")
            return

        pr.addFeatures(feats)
        vl.updateExtents()

        # Style
        sym = QgsFillSymbol.createSimple({
            "color": "0,200,255,60",
            "outline_color": "0,255,255,255",
            "outline_width": "1.6",
        })
        vl.setRenderer(QgsSingleSymbolRenderer(sym))

        QgsProject.instance().addMapLayer(vl)

        # Zoom to combined extent (project CRS-aware)
        try:
            proj = QgsProject.instance()
            tr = QgsCoordinateTransform(vl.crs(), proj.crs(), proj)
            ext_proj = tr.transformBoundingBox(vl.extent())
            self.iface.mapCanvas().setExtent(ext_proj if not ext_proj.isEmpty() else vl.extent())
        except Exception:
            self.iface.mapCanvas().setExtent(vl.extent())
        self.iface.mapCanvas().refresh()

        if bad:
            QMessageBox.warning(self.iface.mainWindow(), "Some IDs skipped",
                                f"{len(bad)} invalid H3 indexes were ignored:\n" +
                                ", ".join(bad[:10]) + ("…" if len(bad) > 10 else ""))
