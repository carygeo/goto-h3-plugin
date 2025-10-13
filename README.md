# GoToH3 — QGIS Plugin

Quickly navigate to one or many Uber H3 cells in QGIS.  
Paste H3 indexes, visualize their hex boundaries, record resolutions, and zoom automatically.

![GoToH3 plugin screenshot](https://raw.githubusercontent.com/carygeo/goto-h3-plugin/main/goto_h3_plugin/screenshot.png)

## Overview

GoToH3 adds a toolbar button and menu entry under **Plugins → H3 Tools**.
It lets you jump directly to any H3 index — or a whole list of them — without leaving QGIS.

You can:

* Paste one or many H3 indexes (comma, space, or newline-separated)
* Instantly visualize their polygon boundaries in **EPSG:4326**
* Automatically populate the attribute table with:

  * `h3` — the H3 index string
  * `res` — the numeric H3 resolution
* Automatically zoom to the combined extent
* Keep the layer styled with a translucent cyan outline for easy inspection

---

## Installation

### From QGIS Plugin Manager (recommended)

1. Open **QGIS → Plugins → Manage and Install Plugins**
2. Search for **“GoToH3”**
3. Click **Install**

### Manual install (for development or testing)

1. Clone or download this repository.
2. Copy the folder into your QGIS plugin directory:

   * **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
   * **Windows**: `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`
   * **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
3. Restart QGIS and enable **GoToH3** under **Plugins → Manage and Install Plugins → Installed**.

---

## Usage

1. Click the **Go To H3 Cell(s)** toolbar button (or find it under *Plugins → H3 Tools*).
2. Paste one or many H3 indexes, separated by commas, spaces, or newlines:

   ```
   8928308280fffff
   8928308280b3fff, 8928308280b7fff
   ```
3. Press **OK**.
4. A new memory layer is created with the polygons and attributes:

   | h3              | res |
   | --------------- | --- |
   | 8928308280fffff | 9   |
   | 8928308280b3fff | 9   |

---

## Requirements

* QGIS ≥ 3.22
* Python ≥ 3.9
* Python package: [`h3`](https://pypi.org/project/h3/) (v3 or v4 supported)

---

## Development

To develop or modify the plugin:

```bash
# Clone
git clone https://github.com/carygeo/goto-h3-plugin.git
cd goto-h3-plugin

# Optional: run validation
pip install qgis-plugin-ci
qgis-plugin-ci validate
```

To reload quickly inside QGIS, install the **Plugin Reloader** plugin and hit *Reload* after edits.

---

## License

This plugin is released under the **GPL-2.0-or-later** license (same as QGIS).

---

## Author

**Cary Greenwood**
Email: [carygreenwood@gmail.com](mailto:carygreenwood@gmail.com)
GitHub: [@carygeo](https://github.com/carygeo)

---

## Changelog

| Version | Date       | Notes                                                   |
| ------- | ---------- | ------------------------------------------------------- |
| 0.2.0   | 2025-10-13 | Added multi-index input and `res` column for resolution |
| 0.1.0   | 2025-08-14 | Initial release — single-cell navigation                |

---

### Tip

Use this plugin alongside H3-based vector datasets to QA spatial coverage, debug tile boundaries, or validate resolution consistency.
