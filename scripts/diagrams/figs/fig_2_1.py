"""Figure 2.1: a seat-map latency distribution, with its mean, median and p99."""
import math
from statistics import NormalDist

from chartkit import Plot
from dg import Diagram
from registry import figure

# Cache hits and misses as a lognormal mixture: share, median ms, sigma.
HIT = (0.92, 38, 0.35)
MISS = (0.08, 700, 0.9)


def cdf(ms):
    return sum(f * NormalDist().cdf((math.log(ms) - math.log(m)) / s) for f, m, s in (HIT, MISS))


def quantile(p):
    lo, hi = 1.0, 1e5
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        lo, hi = (mid, hi) if cdf(mid) < p else (lo, mid)
    return lo


@figure
def fig_2_1():
    mean = sum(f * m * math.exp(s * s / 2) for f, m, s in (HIT, MISS))
    p50, p99 = quantile(0.5), quantile(0.99)
    d = Diagram("fig-2-1", 864, 340, "A latency distribution and the numbers that summarize it",
                f"A seat-map service's latency on a log scale has two humps: cache hits around 40 ms and cache "
                f"misses around 700 ms with a long tail. The median is about {p50:.0f} ms and the mean about "
                f"{mean:.0f} ms, where almost no request falls; the p99 is about 2 s.")
    lg = math.log10
    p = Plot(d, x=72, y=40, w=744, h=232, xr=(lg(10), lg(10000)), yr=(0, 16))
    ticks = [10, 30, 100, 300, 1000, 3000, 10000]
    p.axes(xticks=[lg(t) for t in ticks], yticks=[0, 4, 8, 12, 16],
           xlabel="LATENCY (MS, LOG SCALE)", ylabel="SHARE OF REQUESTS PER BIN (%)",
           xfmt=lambda v: f"{round(10 ** v):,}", yfmt=lambda t: f"{t}%")
    step = 0.05
    edges = [1 + i * step for i in range(int(3 / step) + 1)]
    pts = []
    for a, b in zip(edges, edges[1:]):
        share = 100 * (cdf(10 ** b) - cdf(10 ** a))
        pts += [(a, share), (b, share)]
    p.area(pts, kind="soft")
    p.line(pts, kind="ink", width=1.2)
    p.vline(lg(p50), f"P50 ≈ {round(p50, -1):.0f} MS", at=0.04)
    p.vline(lg(mean), f"MEAN ≈ {round(mean, -1):.0f} MS", at=0.04)
    p.vline(lg(p99), "P99 ≈ 2 S", kind="accent", at=0.04)
    p.annotate(lg(40), 12.5, "CACHE HITS · 92%", dx=-100, dy=-6)
    p.annotate(lg(700), 1.6, "CACHE MISSES · 8%, A LONG TAIL", dx=-80, dy=-10)
    return d
