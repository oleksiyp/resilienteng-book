"""Figure 4.1: Knight Capital's eight SMARS servers, before the open, at the open and after the rollback."""
from html import escape

from dg import Diagram
from registry import figure


@figure
def fig_4_1():
    d = Diagram("fig-4-1", 864, 432, "Knight Capital's eight servers",
                "Three columns show Knight's eight order-router servers. Before 1 August the new code reached "
                "seven servers, and the eighth kept the old code with the dormant Power Peg function. At the "
                "09:30 open, seven servers handled the new orders correctly while the eighth woke Power Peg. "
                "After engineers rolled the seven back to the old code, all eight ran Power Peg until it was "
                "stopped about 45 minutes after the open.")
    cols = [(136, "BEFORE THE OPEN · MANUAL DEPLOY"), (376, "09:30 · MARKET OPENS"), (616, "AFTER THE ROLLBACK")]
    CW, RH, Y0, STEP = 216, 24, 68, 32
    for x, label in cols:
        d.zone(x - 8, 48, CW + 16, 8 * STEP + 24, label)
    cells = {  # phase -> per-server (text, kind)
        0: [("new code", "backend")] * 7 + [("old code · dormant Power Peg", "optional")],
        1: [("new orders handled", "backend")] * 7 + [("Power Peg: child orders, no stop", "accent")],
        2: [("old code · Power Peg", "accent")] * 8,
    }
    accent = []
    for ph, (x, _) in enumerate(cols):
        for i, (text, kind) in enumerate(cells[ph]):
            y = Y0 + i * STEP
            if kind == "accent":
                accent.append(f"M {x + 4},{y} h {CW - 8} a 4 4 0 0 1 4 4 v {RH - 8} a 4 4 0 0 1 -4 4 "
                              f"h -{CW - 8} a 4 4 0 0 1 -4 -4 v -{RH - 8} a 4 4 0 0 1 4 -4 z")
            else:
                dash = ' stroke-dasharray="4,3"' if kind == "optional" else ""
                d.nodes.append(f'<rect class="dg-n dg-n-{kind}" x="{x}" y="{y}" width="{CW}" height="{RH}" rx="4"{dash}/>')
            d.extra.append(f'<text class="dg-sub" x="{x + CW // 2}" y="{y + 15}">{escape(text)}</text>')
    # every Power Peg cell is one accent element
    d.nodes.append(f'<path class="dg-ill-fill-accent" d="{" ".join(accent)}"/>')
    for i in range(8):
        d.note(24, Y0 + i * STEP + 15, f"SMARS server {i + 1}")
    d.note(244, 344, "no second check, no comparison", anchor="middle")
    d.note(244, 360, "97 Power Peg emails, unread", anchor="middle")
    d.note(484, 344, "new orders carry the reused flag", anchor="middle")
    d.note(724, 344, "stopped ≈ 45 min after the open", anchor="middle")
    d.note(724, 360, "4 million executions · 154 stocks", anchor="middle")
    d.legend([("backend", "New code, as intended"), ("optional", "Old code, Power Peg dormant"),
              ("focal", "Power Peg running")])
    return d
