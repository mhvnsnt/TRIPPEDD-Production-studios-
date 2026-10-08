#!/usr/bin/env python3
"""make_viseme_charts.py — per-character Preston Blair mouth-shape charts.

Anim Pull Wave 2, Lane B. Animator deliverable: one 3x3 mouth chart per
Wizard Gang EP02 character (Static / Cipher / Sombra Negra / Narrator),
same viseme set as the lip-sync pipeline (tools/lipsync/VISEME_REFERENCE.md).

Outputs SVG + PNG into tools/lipsync/viseme_charts/.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, Polygon, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "viseme_charts")
os.makedirs(OUT, exist_ok=True)

# (code, title, example sounds)
SHAPES = [
    ("A", "AI — wide open", "fire, see"),
    ("B", "MBP — lips pressed", "baby, move"),
    ("C", "E — teeth apart", "everybody"),
    ("D", "U — rounded", "you, council"),
    ("E", "O — rounded open", "or, more"),
    ("F", "L — tongue on teeth", "like, signal"),
    ("G", "FV — lip under teeth", "fire, five"),
    ("H", "WQ — puckered", "bat, was"),
    ("X", "REST — neutral", "silence"),
]

CHARACTERS = {
    "static": {
        "name": "STATIC", "sub": "Enzo-based · human, clean cartoon mouths",
        "skin": "#c98d64", "lip": "#8a4a3a", "inner": "#5e1f1a",
        "teeth": "#f2ede2", "feral": False, "mask": False, "hood": False,
    },
    "cipher": {
        "name": "CIPHER", "sub": "Lio Rush feral Blackheart · jagged teeth, snarl",
        "skin": "#8a5a3c", "lip": "#5e2f28", "inner": "#3d100d",
        "teeth": "#efe8d8", "feral": True, "mask": False, "hood": False,
    },
    "sombra": {
        "name": "SOMBRA NEGRA", "sub": "luchador · black mask, mouth cutout",
        "skin": "#b97f52", "lip": "#7a3f30", "inner": "#471712",
        "teeth": "#f2ede2", "feral": False, "mask": True, "hood": False,
    },
    "narrator": {
        "name": "NARRATOR", "sub": "purple robe · face in hood shadow, voice-only",
        "skin": "#4a3a55", "lip": "#2e2138", "inner": "#120a18",
        "teeth": "#cfc4d6", "feral": False, "mask": False, "hood": True,
    },
}


def teeth_row(ax, x0, x1, y, n, color, jagged=False):
    w = (x1 - x0) / n
    for i in range(n):
        xa, xb = x0 + i * w, x0 + (i + 1) * w
        if jagged:
            ax.add_patch(Polygon([[xa, y], [xb, y], [(xa + xb) / 2, y - 0.09]],
                                 fc=color, ec="#222", lw=0.6, zorder=4))
        else:
            ax.add_patch(Rectangle((xa, y - 0.055), w, 0.055, fc=color,
                                   ec="#222", lw=0.6, zorder=4))


def draw_mouth(ax, code, st):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    skin, lip, inner, teeth = st["skin"], st["lip"], st["inner"], st["teeth"]
    feral = st["feral"]

    # face backdrop per character
    if st["mask"]:
        ax.add_patch(Rectangle((0.05, 0.05), 0.9, 0.9, fc="#151318",
                               ec="#8f8f9a", lw=2.5, zorder=0))       # mask fabric
        ax.add_patch(Rectangle((0.05, 0.05), 0.9, 0.9, fc="none",
                               ec="#c0c0cc", lw=0.8, linestyle="--", zorder=5))
        ax.add_patch(Ellipse((0.5, 0.42), 0.62, 0.5, fc=skin, ec="#0a0a0c",
                             lw=2, zorder=1))                          # mouth cutout
    elif st["hood"]:
        ax.add_patch(Rectangle((0.05, 0.05), 0.9, 0.9, fc="#1c1226", zorder=0))
        ax.add_patch(Ellipse((0.5, 0.55), 0.78, 0.9, fc="#2b1b3d",
                             ec="#6b4a8f", lw=2.5, zorder=1))           # hood
        ax.add_patch(Ellipse((0.5, 0.42), 0.55, 0.5, fc="#241a30", zorder=2))  # shadowed face
    else:
        ax.add_patch(Ellipse((0.5, 0.5), 0.9, 0.95, fc=skin, ec="#2a1a12",
                             lw=2, zorder=0))

    cx = 0.5
    lw_lip = 2.2

    if code == "A":  # wide open
        ax.add_patch(Ellipse((cx, 0.40), 0.34, 0.42, fc=inner, ec=lip,
                             lw=lw_lip, zorder=3))
        teeth_row(ax, cx - 0.13, cx + 0.13, 0.585, 5, teeth, feral)
        ax.add_patch(Ellipse((cx, 0.24), 0.16, 0.10, fc="#a34a44", zorder=3))  # tongue
    elif code == "B":  # pressed
        ax.plot([cx - 0.17, cx + 0.17], [0.40, 0.40], c=lip, lw=4,
                solid_capstyle="round", zorder=3)
        ax.plot([cx - 0.17, cx + 0.17], [0.43, 0.43], c=skin, lw=1.2, zorder=4)
    elif code == "C":  # teeth slightly apart
        ax.add_patch(Ellipse((cx, 0.40), 0.30, 0.13, fc=inner, ec=lip,
                             lw=lw_lip, zorder=3))
        teeth_row(ax, cx - 0.12, cx + 0.12, 0.455, 5, teeth, False)
    elif code == "D":  # rounded small
        ax.add_patch(Circle((cx, 0.40), 0.075, fc=inner, ec=lip, lw=lw_lip, zorder=3))
    elif code == "E":  # rounded open
        ax.add_patch(Ellipse((cx, 0.40), 0.20, 0.26, fc=inner, ec=lip,
                             lw=lw_lip, zorder=3))
        if feral:
            teeth_row(ax, cx - 0.07, cx + 0.07, 0.52, 3, teeth, True)
        ax.add_patch(Ellipse((cx, 0.30), 0.09, 0.06, fc="#a34a44", zorder=3))
    elif code == "F":  # tongue on teeth
        ax.add_patch(Ellipse((cx, 0.40), 0.30, 0.14, fc=inner, ec=lip,
                             lw=lw_lip, zorder=3))
        teeth_row(ax, cx - 0.12, cx + 0.12, 0.46, 5, teeth, False)
        ax.add_patch(Rectangle((cx - 0.05, 0.40), 0.10, 0.09, fc="#c06a5e",
                               ec="#7a3a34", lw=1, zorder=4))          # tongue tip
    elif code == "G":  # lower lip under upper teeth
        teeth_row(ax, cx - 0.11, cx + 0.11, 0.475, 5, teeth, feral)
        ax.add_patch(Ellipse((cx, 0.345), 0.26, 0.10, fc=lip, ec="#4a2420",
                             lw=1.6, zorder=4))                        # tucked lower lip
    elif code == "H":  # puckered
        ax.add_patch(Ellipse((cx, 0.40), 0.15, 0.11, fc=inner, ec=lip,
                             lw=lw_lip + 0.6, zorder=3))
        for dx in (-0.10, 0.10):  # pucker creases
            ax.plot([cx + dx, cx + dx * 1.6], [0.40, 0.40], c=lip, lw=1.2, zorder=3)
    else:  # X rest
        ax.plot([cx - 0.14, cx + 0.14], [0.40, 0.40], c="#3a2620" if not st["hood"] else "#0e0812",
                lw=2.4, solid_capstyle="round", zorder=3)


def make_chart(key):
    st = CHARACTERS[key]
    fig, axes = plt.subplots(3, 3, figsize=(10, 11))
    fig.patch.set_facecolor("#f4f1ea")
    fig.suptitle(f"{st['name']} — MOUTH-SHAPE CHART", fontsize=18,
                 fontweight="bold", y=0.97)
    fig.text(0.5, 0.935, st["sub"], ha="center", fontsize=10, style="italic")
    fig.text(0.5, 0.915,
             "Preston Blair viseme set — drive frame-by-frame from the timeline JSON "
             "(start/end/viseme); hold X = neutral, do not animate through X.",
             ha="center", fontsize=8.5, color="#444")
    for ax, (code, title, ex) in zip(axes.flat, SHAPES):
        draw_mouth(ax, code, st)
        ax.set_title(f"{code} — {title}\n({ex})", fontsize=9, pad=4)
    plt.tight_layout(rect=[0, 0.02, 1, 0.90])
    fig.text(0.5, 0.005,
             "TRIPPEDD lipsync · tools/lipsync/viseme_charts/ · "
             "phoneme→viseme mapping: VISEME_REFERENCE.md",
             ha="center", fontsize=7.5, color="#666")
    base = os.path.join(OUT, f"viseme_chart_{key}")
    fig.savefig(base + ".png", dpi=200)
    fig.savefig(base + ".svg")
    plt.close(fig)
    print("wrote", base + ".png/.svg")


if __name__ == "__main__":
    for k in CHARACTERS:
        make_chart(k)
