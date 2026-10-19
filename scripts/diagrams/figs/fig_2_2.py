"""Figure 2.2: queueing delay against utilization — the hockey stick."""
from chartkit import Plot
from dg import Diagram
from registry import figure


@figure
def fig_2_2():
    d = Diagram("fig-2-2", 864, 328, "Response time against utilization",
                "For one server with random arrivals and service times, response time is the service time divided "
                "by one minus the utilization: twice the service time at 50%, five times at 80%, ten at 90% and 25 "
                "at 96%. Burstier arrivals, per Kingman, steepen the curve further. Encore's write shards are "
                "planned at 80%; a hot shard taking 30% of writes instead of 25% runs at 96%.")
    p = Plot(d, x=72, y=40, w=744, h=240, xr=(0, 1), yr=(0, 30))
    p.axes(xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=[0, 5, 10, 15, 20, 25, 30],
           xlabel="UTILIZATION OF THE SERVER", ylabel="RESPONSE TIME (× SERVICE TIME)",
           xfmt=lambda v: f"{round(v * 100)}%", yfmt=lambda t: f"{t}×")
    rho = [i / 1000 for i in range(0, 968)]
    p.line([(r, 1 + 2 * r / (1 - r)) for r in rho if 1 + 2 * r / (1 - r) <= 18], kind="soft", dashed=True)
    p.line([(r, 1 / (1 - r)) for r in rho], kind="ink")
    for r, txt in ((0.9, "10× AT 90%"),):
        p.dot(r, 1 / (1 - r), kind="ink", r=3.5)
        p.annotate(r, 1 / (1 - r), txt, dx=8, dy=14)
    p.dot(0.95, 20, kind="ink", r=3.5)
    p.annotate(0.95, 20, "20× AT 95%", dx=-10, dy=3, anchor="end")
    p.dot(0.8, 5, kind="accent")
    p.annotate(0.8, 5, "WRITE SHARDS: 80% → 5×", dx=8, dy=14, kind="accent")
    p.dot(0.96, 25)
    p.annotate(0.96, 25, "HOT SHARD AT 96% → 25×", dx=-10, dy=3, anchor="end")
    p.annotate(0.894, 1 + 2 * 0.894 / 0.106, "BURSTY ARRIVALS (KINGMAN)", dx=-8, dy=-4, anchor="end")
    return d
