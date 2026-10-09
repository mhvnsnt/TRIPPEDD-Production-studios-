"""
THE MEASURED MOUTH FRAME — shared by everything that builds oral anatomy.

Mars's scan is not axis-aligned. His mouth line is rolled 5.61 degrees off
horizontal, his mouth centre is at world x -0.021, and his ears are at local
x -1.23 and +1.60 mouth-widths: the head is genuinely asymmetric. A dental arch
laid out on world X/Y/Z lands visibly crooked inside a head that is not, and the
"why does it look wrong" is invisible in every number you might print.

So: one frame, derived from the inner-lip contour MediaPipe found on the real
surface, and every piece of anatomy expressed in it.

    x  mouth-right      y  into the head      z  mouth-up
    origin: the centroid of the measured oral aperture
    unit of choice: MW, the measured mouth width (0.1930)
"""
import json, os, math, mathutils

V = mathutils.Vector

class MouthFrame:
    def __init__(self, path="renders/_rig_measure/mouth_anatomy.json", slit_z=0.42):
        self.raw = json.load(open(os.path.abspath(path)))
        f = self.raw["frame"]
        self.M = mathutils.Matrix(f["matrix"])
        self.Mi = self.M.inverted()
        self.MW = self.raw["aperture"]["width"]
        self.slit_z = slit_z
        c = self.raw["contours"]
        self.inner_up = [self.local(p) for p in c["lip_inner_upper"]]
        self.inner_lo = [self.local(p) for p in c["lip_inner_lower"]]
        self.outer_up = [self.local(p) for p in c["lip_outer_upper"]]
        self.outer_lo = [self.local(p) for p in c["lip_outer_lower"]]
        self.corner_l = self.inner_up[0]
        self.corner_r = self.inner_up[-1]
        self.cx = sum(p.x for p in self.inner_up + self.inner_lo) / (len(self.inner_up) + len(self.inner_lo))
        # The lip SEAM as a curve, not a plane. The corners of a mouth sit lower
        # and deeper than its centre; treating the seam as z = 0 puts the upper
        # lip on the wrong side of it near the corners, and those verts then ride
        # the jaw and drag the top lip down with the bottom one.
        self._seam = sorted([(u.x, self.slit_z * 0.5 * (u.z + l.z))
                             for u, l in zip(self.inner_up, self.inner_lo)])
        # How tall the CUT is at each x. The weighting band must never be wider
        # than this: if it is, the vertices the boolean put on the lip edge land
        # mid-blend and come out at weight 0.65 instead of 1.0 — which is the
        # lower lip only two-thirds committed to the jaw, and a mouth that
        # opens two-thirds of the way to not at all.
        self._gap = sorted([(u.x, abs(self.slit_z * (u.z - l.z)))
                            for u, l in zip(self.inner_up, self.inner_lo)])

    def local(self, p): return self.Mi @ V(p)
    def world(self, p): return self.M @ V(p)

    @staticmethod
    def _interp(curve, x):
        if x <= curve[0][0]: return curve[0][1]
        if x >= curve[-1][0]: return curve[-1][1]
        for (x0, z0), (x1, z1) in zip(curve, curve[1:]):
            if x0 <= x <= x1:
                t = 0.0 if x1 == x0 else (x - x0) / (x1 - x0)
                return z0 + t * (z1 - z0)
        return curve[-1][1]

    def seam_z(self, x):
        return self._interp(self._seam, x)

    def slit_gap(self, x):
        return self._interp(self._gap, x)

    def aperture_distance(self, p):
        """Shortest distance in the local XZ plane to the measured aperture curve."""
        best = 1e18
        for q in self.inner_up + self.inner_lo:
            d = (p.x - q.x) ** 2 + (p.z - q.z) ** 2
            if d < best: best = d
        return math.sqrt(best)


def smoothstep(u):
    if u <= 0.0: return 0.0
    if u >= 1.0: return 1.0
    return u * u * (3.0 - 2.0 * u)
