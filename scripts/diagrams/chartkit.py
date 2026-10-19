"""Charts and illustrations on top of dg.Diagram, in the same skin.

A Plot maps data coordinates into a pixel rectangle of the figure and draws axes, gridlines,
series, shaded bands, markers and annotations with dg-* classes, so charts follow the book's
light and dark themes like every other figure. Keep the diagram rules: at most two accent
elements per figure, labels on opaque masks, legend strip at the bottom (Diagram.legend).

    d = Diagram("fig-6-1", 864, 400, title, desc)
    p = Plot(d, x=72, y=32, w=744, h=280, xr=(0, 1), yr=(0, 20))
    p.axes(xticks=[0, .5, 1], yticks=[0, 10, 20], xlabel="UTILIZATION", ylabel="WAIT (× SERVICE TIME)")
    p.line([(u, u / (1 - u)) for u in ...], kind="accent")
    p.annotate(0.8, 4, "80% — the knee")
Raw SVG is also fine for illustrations (d.extra.append(...)) as long as it uses the dg-* classes
defined in dg.css: dg-ill-ink, dg-ill-soft, dg-ill-accent, dg-ill-link, dg-ill-fill, dg-ill-fill-accent.
"""
from html import escape

from dg import label_width


class Plot:
    def __init__(self, d, x, y, w, h, xr, yr, ylog=False):
        self.d, self.x, self.y, self.w, self.h = d, x, y, w, h
        self.xr, self.yr, self.ylog = xr, yr, ylog

    def px(self, vx):
        return self.x + (vx - self.xr[0]) / (self.xr[1] - self.xr[0]) * self.w

    def py(self, vy):
        import math
        if self.ylog:
            a, b = math.log10(self.yr[0]), math.log10(self.yr[1])
            return self.y + self.h - (math.log10(vy) - a) / (b - a) * self.h
        return self.y + self.h - (vy - self.yr[0]) / (self.yr[1] - self.yr[0]) * self.h

    def pt(self, vx, vy):
        return self.px(vx), self.py(vy)

    def _poly(self, pts):
        return " ".join(f"{self.px(a):.1f},{self.py(b):.1f}" for a, b in pts)

    # ---- frame -------------------------------------------------------------------------------
    def axes(self, xticks=(), yticks=(), xlabel=None, ylabel=None, grid=True, xfmt=str, yfmt=str):
        d, x0, y0, x1, y1 = self.d, self.x, self.y + self.h, self.x + self.w, self.y
        out = []
        if grid:
            for t in yticks:
                yy = self.py(t)
                out.append(f'<line class="dg-grid" x1="{x0}" y1="{yy:.1f}" x2="{x1}" y2="{yy:.1f}"/>')
        out.append(f'<line class="dg-axis" x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}"/>')
        out.append(f'<line class="dg-axis" x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}"/>')
        for t in xticks:
            xx = self.px(t)
            out.append(f'<line class="dg-axis" x1="{xx:.1f}" y1="{y0}" x2="{xx:.1f}" y2="{y0 + 4}"/>')
            out.append(f'<text class="dg-tick" x="{xx:.1f}" y="{y0 + 16}" text-anchor="middle">{escape(xfmt(t))}</text>')
        for t in yticks:
            yy = self.py(t)
            out.append(f'<text class="dg-tick" x="{x0 - 8}" y="{yy + 3:.1f}" text-anchor="end">{escape(yfmt(t))}</text>')
        if xlabel:
            out.append(f'<text class="dg-axis-label" x="{x1}" y="{y0 + 32}" text-anchor="end">{escape(xlabel)}</text>')
        if ylabel:
            out.append(f'<text class="dg-axis-label" x="{x0}" y="{y1 - 10}" text-anchor="start">{escape(ylabel)}</text>')
        d.zones.append("\n".join(out))

    # ---- marks -------------------------------------------------------------------------------
    def line(self, pts, kind="ink", dashed=False, width=None):
        """kind: ink | soft | accent | link"""
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        w = f' stroke-width="{width}"' if width else ""
        self.d.nodes.append(f'<polyline class="dg-series dg-s-{kind}" points="{self._poly(pts)}"{dash}{w}/>')

    def area(self, pts, kind="soft", base=None):
        """Shade between the series and base (default: the bottom of the y range)."""
        b = self.yr[0] if base is None else base
        poly = [(pts[0][0], b), *pts, (pts[-1][0], b)]
        self.d.zones.append(f'<polygon class="dg-area dg-ar-{kind}" points="{self._poly(poly)}"/>')

    def band(self, x0, x1, kind="soft", label=None):
        """A vertical shaded band across the plot (a window, an incident, a freeze)."""
        a, b = self.px(x0), self.px(x1)
        self.d.zones.append(f'<rect class="dg-area dg-ar-{kind}" x="{a:.1f}" y="{self.y}" width="{b - a:.1f}" height="{self.h}"/>')
        if label:
            self.d.label_at(label, (a + b) / 2, self.y + 14, horizontal=True, side="below",
                            kind="accent" if kind == "accent" else "muted")

    def hline(self, vy, label=None, kind="soft", dashed=True, side="above", at=0.98):
        yy = self.py(vy)
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        self.d.nodes.append(f'<line class="dg-series dg-s-{kind}" x1="{self.x}" y1="{yy:.1f}" x2="{self.x + self.w}" y2="{yy:.1f}"{dash}/>')
        if label:
            lw = label_width(label)
            self.d.label_at(label, self.x + self.w * at - lw / 2, yy, horizontal=True, side=side,
                            kind="accent" if kind == "accent" else "muted")

    def vline(self, vx, label=None, kind="soft", dashed=True, at=0.1):
        xx = self.px(vx)
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        self.d.nodes.append(f'<line class="dg-series dg-s-{kind}" x1="{xx:.1f}" y1="{self.y}" x2="{xx:.1f}" y2="{self.y + self.h}"{dash}/>')
        if label:
            self.d.label_at(label, xx, self.y + self.h * at, horizontal=False, side="right",
                            kind="accent" if kind == "accent" else "muted")

    def dot(self, vx, vy, kind="accent", r=4):
        xx, yy = self.pt(vx, vy)
        self.d.nodes.append(f'<circle class="dg-dot dg-dot-{kind}" cx="{xx:.1f}" cy="{yy:.1f}" r="{r}"/>')

    def annotate(self, vx, vy, text, dx=8, dy=-8, kind="muted", anchor="start"):
        """A short mono note near a data point, on a paper mask."""
        xx, yy = self.pt(vx, vy)
        w = label_width(text)
        bx = xx + dx if anchor == "start" else xx + dx - w
        cls = {"accent": "dg-label dg-l-accent", "link": "dg-label dg-l-link"}.get(kind, "dg-label")
        self.d.labels.append(f'<rect class="dg-mask" x="{bx:.1f}" y="{yy + dy - 9:.1f}" width="{w}" height="12" rx="2"/>'
                             f'<text class="{cls}" x="{bx + w / 2:.1f}" y="{yy + dy:.1f}">{escape(text)}</text>')
