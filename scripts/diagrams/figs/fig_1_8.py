"""Figure 1.8: serial composition of availability against the checkout objective."""
from chartkit import Plot
from dg import Diagram
from registry import figure


@figure
def fig_1_8():
    d = Diagram("fig-1-8", 864, 328, "Serial dependencies multiply",
                "The availability of a journey with one to six hard dependencies in series, if their failures are "
                "independent: at 99.95% each, two already reach the 99.9% checkout objective and four give about 99.80%; at 99.99% each, "
                "three give about 99.97%, leaving room inside the objective.")
    p = Plot(d, x=72, y=40, w=744, h=240, xr=(0.5, 6.5), yr=(99.6, 100.0))
    p.axes(xticks=[1, 2, 3, 4, 5, 6], yticks=[99.6, 99.7, 99.8, 99.9, 100.0],
           xlabel="HARD DEPENDENCIES IN SERIES", ylabel="AVAILABILITY IF INDEPENDENT",
           yfmt=lambda t: f"{t:.1f}%")
    p.hline(99.9, "CHECKOUT SLO 99.9%", kind="accent", side="below", at=0.9)
    lo = [(n, 100 * 0.9995 ** n) for n in range(1, 7)]
    hi = [(n, 100 * 0.9999 ** n) for n in range(1, 7)]
    p.line(lo, kind="ink")
    p.line(hi, kind="link")
    for n, v in lo:
        p.dot(n, v, kind="ink", r=3.5)
    for n, v in hi:
        p.dot(n, v, kind="link", r=3.5)
    p.annotate(4, lo[3][1], "FOUR AT 99.95% ≈ 99.80%", dx=-10, dy=16, anchor="end")
    p.annotate(3, hi[2][1], "THREE AT 99.99% ≈ 99.97%", dx=-2, dy=-12, kind="link")
    p.annotate(6, lo[5][1], "EACH AT 99.95%", dx=-10, dy=16, anchor="end")
    p.annotate(6, hi[5][1], "EACH AT 99.99%", dx=-10, dy=-10, kind="link", anchor="end")
    return d
