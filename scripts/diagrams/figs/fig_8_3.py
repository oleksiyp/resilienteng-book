"""Figure 8.3 — the nightly golden-set run when the provider moved the alias."""
from dg import Diagram
from chartkit import Plot
from registry import figure

DAYS = ["THU", "FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU", "FRI"]
RUN = 2 / 24   # the nightly run at 02:00


@figure
def fig_8_3():
    d = Diagram("fig-8-3", 864, 360, "The golden set catches a moved alias",
                "Nightly golden-set pass rates over nine days. Refund cases pass 18 of 18 every night until the "
                "Wednesday run, after the provider moved the cheap tier's alias on Tuesday, when they pass 11 of "
                "18; the overall score dips only from 193 to 186 of 200. The previous snapshot is pinned by "
                "Wednesday lunchtime, about 30 hours after the move, and Thursday's run is back to 18 of 18.")
    p = Plot(d, x=72, y=48, w=744, h=216, xr=(0, 8.6), yr=(40, 112))
    p.axes(xticks=list(range(9)), yticks=[40, 50, 60, 70, 80, 90, 100], xfmt=lambda t: DAYS[t],
           yfmt=lambda v: f"{v}%", ylabel="GOLDEN-SET PASS RATE, NIGHTLY RUN AT 02:00",
           xlabel="ONE WEEK AND A BIT")
    p.band(5 + 6 / 24, 6.5, kind="accent", label="30 H ON THE MOVED ALIAS")
    refund = [(i + RUN, 100.0) for i in range(9)]
    refund[6] = (6 + RUN, 100 * 11 / 18)
    overall = [(i + RUN, 96.5) for i in range(9)]
    overall[6] = (6 + RUN, 93.0)
    p.line(overall, kind="ink")
    p.line(refund, kind="accent")
    for x, y in overall:
        p.dot(x, y, kind="ink", r=3)
    for x, y in refund:
        p.dot(x, y, kind="ink", r=3)
    p.annotate(6 + RUN, 100 * 11 / 18, "REFUND CASES 11 / 18", dx=10, dy=4)
    p.annotate(4.9, 88, "OVERALL 193 → 186 / 200", dx=0, dy=0, anchor="end")
    p.annotate(8 + RUN, 100, "REFUND 18 / 18", dx=0, dy=-8, anchor="end")
    p.vline(6.5, kind="soft")
    p.annotate(6.5, 52, "PINNED BACK", dx=6, dy=0)
    d.legend([("arrow:accent", "Refund cases (18)"), ("arrow:muted", "All cases (200)")])
    return d
