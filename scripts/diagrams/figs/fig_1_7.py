"""Figure 1.7: a multi-window burn-rate page through one incident."""
from chartkit import Plot
from dg import Diagram
from registry import figure

FAULT, FIX, BAD, BASE = 30, 70, 10.0, 0.05   # minutes, minutes, % bad during the fault, % bad otherwise
THRESH = 1.44                                # 14.4 × a 0.1% budget


def ratio(t, window):
    """Mean bad ratio (%) over the last `window` minutes at minute t, for a fault from FAULT to FIX."""
    lo = t - window
    overlap = max(0.0, min(t, FIX) - max(lo, FAULT))
    span = window if lo >= 0 else max(t, 1e-9)
    return BASE + (BAD - BASE) * overlap / span


@figure
def fig_1_7():
    d = Diagram("fig-1-7", 864, 328, "A multi-window burn-rate page through one incident",
                "The seat map serves 10% bad requests from minute 30 to minute 70. The one-hour bad ratio crosses "
                "the 14.4x threshold of 1.44% at about minute 39 and stays above it until about minute 121; the "
                "five-minute ratio drops below it about four minutes after the fix, so the page, which needs both, "
                "fires at minute 39 and resolves at minute 74.")
    p = Plot(d, x=72, y=40, w=744, h=240, xr=(0, 150), yr=(0, 12))
    p.axes(xticks=[0, 30, 60, 90, 120, 150], yticks=[0, 2, 4, 6, 8, 10, 12],
           xlabel="MINUTES", ylabel="BAD REQUESTS (%)", yfmt=lambda t: f"{t}%")
    t_page = FAULT + THRESH / (BAD - BASE) * 60
    t_clear5 = FIX + 5 * (1 - (THRESH - BASE) / (BAD - BASE))
    t_clear60 = 130 - (THRESH - BASE) / (BAD - BASE) * 60
    p.band(t_page, t_clear5, kind="accent", label="PAGE")
    p.band(t_clear5, t_clear60, kind="soft", label="1 H ALONE WOULD STILL PAGE")
    p.hline(THRESH, "14.4× THRESHOLD · 1.44%", side="above", at=1.0)
    ts = [i / 4 for i in range(0, 601)]
    p.line([(t, ratio(t, 5)) for t in ts], kind="link")
    p.line([(t, ratio(t, 60)) for t in ts], kind="ink")
    p.vline(FAULT)
    p.vline(FIX)
    d.label_at("FAULT", p.px(FAULT), p.py(8.5), horizontal=False, side="left")
    d.label_at("FIX", p.px(FIX), p.py(8.5), horizontal=False, side="left")
    p.annotate(30, 10, "5-MINUTE RATIO", dx=-6, dy=3, kind="link", anchor="end")
    p.annotate(100, ratio(100, 60), "1-HOUR RATIO", dx=8, dy=-6)
    return d
