"""Figure 4.4: the canary schedule drawn over time, with a rollback at step 3."""
from chartkit import Plot
from dg import Diagram
from registry import figure


@figure
def fig_4_4():
    d = Diagram("fig-4-4", 864, 380, "A canary over time",
                "Traffic share to the new version on a logarithmic scale against minutes: 1% for at least 10 "
                "minutes and 20,000 requests, 5% for 15 minutes, 25% for 20 minutes, then 100%. A second "
                "canary follows the same steps until an integrity alarm six minutes into the 25% step sends "
                "it straight back to zero.")
    p = Plot(d, x=72, y=48, w=744, h=232, xr=(0, 60), yr=(0.6, 100), ylog=True)
    p.axes(xticks=[0, 10, 25, 45, 60], yticks=[0.6, 1, 5, 25, 100],
           xlabel="MINUTES SINCE DEPLOY", ylabel="TRAFFIC TO THE NEW VERSION (LOG SCALE)",
           yfmt=lambda t: "0" if t < 1 else f"{t:g}%")
    p.band(0, 10, label="STEP 1 · ≥ 20,000 REQ")
    p.band(25, 45, label="STEP 3 · BURN < 2×")
    ok = [(0, 1), (10, 1), (10, 5), (25, 5), (25, 25), (45, 25), (45, 100), (60, 100)]
    bad = [(25, 25), (31, 25), (31, 0.6)]
    p.line(ok, kind="ink")
    p.line(bad, kind="accent")
    p.annotate(31, 3, "INTEGRITY ALARM → 0%", dx=8, dy=0, kind="accent")
    p.annotate(10, 5, "5% · 15 MIN", dx=8, dy=-8)
    p.annotate(45, 100, "100% · NORMAL BURN ALERTS", dx=8, dy=14)
    d.legend([("arrow:muted", "Promoted: every step held"), ("arrow:accent", "Rolled back at step 3"),
              ("input", "Minimum bake")])
    return d
