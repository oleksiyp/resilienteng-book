"""Figure 3.1: three governors on Catalog's replica count."""
from chartkit import Plot
from dg import Diagram
from registry import figure


@figure
def fig_3_1():
    d = Diagram("fig-3-1", 864, 372, "Three governors on one lever",
                "A sketch of Catalog's replica count over half an hour. An engineer scales it from 20 to 60; "
                "within seconds the GitOps agent restores the manifest's 20. When browsing ebbs, the autoscaler "
                "waits out its five-minute scale-down window and then trims toward its floor of 12; the GitOps "
                "agent restores 20 within seconds, and the two trade the count several times a minute for the "
                "rest of the half hour, while the engineer believes the service is at 60.")
    p = Plot(d, x=72, y=40, w=744, h=232, xr=(0, 36), yr=(0, 70))
    p.axes(xticks=[0, 6, 12, 18, 24, 30, 36], yticks=[0, 12, 20, 40, 60],
           xlabel="MINUTES", ylabel="CATALOG REPLICAS")
    p.band(6, 11)
    pts = [(0, 20), (3, 20), (3, 60), (3.15, 60), (3.15, 20), (11, 20)]
    t = 11.0
    while t < 36:
        pts += [(t, 20), (t, 12), (t + 0.12, 12), (t + 0.12, 20)]
        t += 0.4
    pts.append((36, 20))
    p.hline(60, "WHAT THE ENGINEER BELIEVED", side="above", at=0.82)
    p.hline(12, "HPA FLOOR", side="below", at=0.97)
    p.line(pts, kind="accent")
    p.annotate(3, 60, "KUBECTL SCALE → 60", dx=8, dy=-8, kind="accent")
    p.annotate(3.15, 40, "GITOPS REVERTS IN SECONDS", dx=8, dy=3)
    p.annotate(6, 20, "BROWSING EBBS", dx=4, dy=-10)
    p.annotate(6, 48, "5-MIN SCALE-DOWN WINDOW", dx=4, dy=0)
    p.annotate(14, 20, "HPA TRIMS, GITOPS RESTORES, SEVERAL TIMES A MINUTE", dx=0, dy=-14, anchor="start")
    d.legend([("arrow:accent", "Actual replicas"), ("arrow:muted:dashed", "Belief and floor")])
    return d
