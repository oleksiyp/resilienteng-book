"""Figure 2.4: the USL fitted to one Seat Inventory shard, with the measured points."""
from chartkit import Plot
from dg import Diagram
from registry import figure

SIGMA, KAPPA, X1 = 0.03, 0.0005, 120
MEASURED = [(1, 121), (4, 431), (8, 790), (16, 1210), (32, 1570), (64, 1540)]


def usl(n, kappa=KAPPA):
    return X1 * n / (1 + SIGMA * (n - 1) + kappa * n * (n - 1))


@figure
def fig_2_4():
    d = Diagram("fig-2-4", 864, 352, "Where one shard stops scaling",
                "Measured write throughput of one Seat Inventory shard at six concurrency levels, with the "
                "Universal Scalability Law fitted at sigma 0.03 and kappa 0.0005. Linear scaling and Amdahl's law "
                "(contention only) rise far above the measurements; the fitted curve peaks at about 1,630 writes/s "
                "near 44 writers and falls beyond. The concurrency cap sits at 32, just under the peak.")
    p = Plot(d, x=72, y=40, w=744, h=240, xr=(0, 100), yr=(0, 2400))
    p.axes(xticks=[0, 16, 32, 48, 64, 80, 96], yticks=[0, 600, 1200, 1800, 2400],
           xlabel="CONCURRENT WRITERS N", ylabel="WRITES PER SECOND", yfmt=lambda t: f"{t:,}")
    p.line([(0, 0), (20, 2400)], kind="soft", dashed=True)
    p.annotate(17.5, 2100, "LINEAR", dx=-8, dy=0, anchor="end")
    amd = [(n, usl(n, 0)) for n in range(1, 101) if usl(n, 0) <= 2400]
    p.line(amd, kind="soft", dashed=True)
    p.annotate(amd[-1][0], amd[-1][1], "AMDAHL: CONTENTION ONLY", dx=8, dy=4)
    p.hline(1500, "PUBLISHED 1.5K WRITES/S", side="below", at=0.9)
    p.vline(32, "CONCURRENCY CAP 32", at=0.92)
    p.line([(n / 2, usl(n / 2)) for n in range(2, 201)], kind="ink")
    for n, v in MEASURED:
        p.dot(n, v, kind="link", r=3.5)
    p.dot(44, usl(44), kind="accent", r=4.5)
    p.annotate(44, usl(44), "PEAK ≈ 1,630/S AT N ≈ 44", dx=8, dy=-10, kind="accent")
    p.annotate(98, usl(98), "RETROGRADE: MORE WRITERS, LESS WORK", dx=0, dy=18, anchor="end")
    d.legend([("arrow:muted", "USL fit (σ 0.03, κ 0.0005)"), ("arrow:link", "Measured (dots)")])
    return d
