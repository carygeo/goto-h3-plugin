#!/usr/bin/env python3
import os, math
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))

def hex_points(cx, cy, r):
    # flat-top hex
    return [(cx + r*math.cos(math.radians(60*i)),
             cy + r*math.sin(math.radians(60*i))) for i in range(6)]

def make_icon(size, radius, filename):
    path = os.path.join(HERE, filename)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pts = hex_points(size/2, size/2, radius)
    pts = [(int(round(x)), int(round(y))) for (x, y) in pts]

    # outline thickness scales with size
    stroke = max(2, size // 12)

    # draw hex edges (bright cyan on transparent)
    for i in range(6):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % 6]
        draw.line([x1, y1, x2, y2], fill=(0, 255, 255, 255), width=stroke)

    img.save(path, "PNG")
    print(f"Wrote {path}")

if __name__ == "__main__":
    make_icon(24, 9, "icon.png")      # toolbar icon
    make_icon(48, 18, "icon@2x.png")  # HiDPI

