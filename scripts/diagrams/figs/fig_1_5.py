"""Figure 1.5: the On-Sale team's error budget across a 28-day window, and the spring burn."""
from chartkit import Plot
from dg import Diagram
from registry import figure


@figure
def fig_1_5():
    d = Diagram("fig-1-5", 864, 328, "An error budget burned down by someone else's change",
                "The On-Sale team's 28-day error budget falls slowly with ordinary spending until a Bot Screening "
                "rule blocks real fans and takes 70% of it in 15 minutes, leaving about 23%, below the policy's 25% "
                "review threshold; a dashed diagonal shows the steady burn that would spend exactly the whole "
                "budget in the window.")
    p = Plot(d, x=72, y=40, w=744, h=240, xr=(0, 28), yr=(0, 100))
    p.axes(xticks=[0, 7, 14, 21, 28], yticks=[0, 25, 50, 75, 100],
           xlabel="DAY OF THE 28-DAY WINDOW", ylabel="BUDGET REMAINING (%)", yfmt=lambda t: f"{t}%")
    p.line([(0, 100), (28, 0)], kind="soft", dashed=True)
    p.annotate(17, 39, "BURN RATE 1: SPENT EXACTLY AT DAY 28", dx=8, dy=-4)
    p.hline(25, "BELOW 25%: SRE PEER REVIEW", side="above", at=0.62)
    p.hline(0, "AT 0%: RELIABILITY WORK ONLY", side="above", at=0.62, dashed=False)
    p.line([(0, 100), (3, 98), (6, 95.5), (9, 93), (9.01, 23), (12, 22), (15, 21), (18, 19.5), (21, 18.5),
            (24, 17.5), (28, 16)], kind="accent")
    p.annotate(9, 85, "BOT SCREENING RULE: 70% IN 15 MIN", dx=10, dy=0, kind="accent")
    p.annotate(9, 23, "≈23% LEFT · ON-SALE UNDER REVIEW", dx=8, dy=18)
    p.annotate(5, 96.5, "ORDINARY SPENDING", dx=0, dy=-7)
    return d
