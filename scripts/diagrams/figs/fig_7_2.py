"""Figure 7.2: how long each kind of credential lives, on a log scale, against the Rowmate revocation."""
from math import log10

from dg import Diagram
from chartkit import Plot
from registry import figure

MIN, HOUR, DAY, MONTH, YEAR = 1, 60, 1440, 43800, 525600


@figure
def fig_7_2():
    d = Diagram("fig-7-2", 864, 348, "Credential lifetimes against a 38-minute revocation",
                "Lifetimes on a logarithmic scale from one minute to beyond a year. Rowmate's static API key had "
                "lived 26 months and would have lived until someone revoked it; Encore revoked it 38 minutes "
                "after the leak. A partner OAuth token lives 15 minutes, a workload SVID one hour, renewed at "
                "half-life, and a break-glass session 60 minutes.")
    p = Plot(d, x=200, y=56, w=632, h=200, xr=(0, 6.3), yr=(0, 4))
    ticks = [(MIN, "1 MIN"), (15, "15 MIN"), (HOUR, "1 H"), (DAY, "1 DAY"), (MONTH, "1 MONTH"), (YEAR, "1 YEAR")]
    lab = {log10(v): t for v, t in ticks}
    p.axes(xticks=list(lab), xfmt=lambda t: lab[t], xlabel="LIFETIME (LOG SCALE)", grid=False)
    for v, _ in ticks[1:]:
        xx = p.px(log10(v))
        d.zones.append(f'<line class="dg-grid" x1="{xx:.1f}" y1="{p.y}" x2="{xx:.1f}" y2="{p.y + p.h}"/>')
    # the revocation
    xr = p.px(log10(38))
    d.nodes.append(f'<line class="dg-series dg-s-accent" x1="{xr:.1f}" y1="{p.y - 4}" x2="{xr:.1f}" '
                   f'y2="{p.y + p.h}" stroke-dasharray="5 4"/>')
    d.label_at("ROWMATE KEY REVOKED · 38 MIN AFTER THE LEAK", xr, p.y - 4, horizontal=True, side="above",
               kind="accent")
    rows = [("Rowmate API key", "static · scoped", 26 * MONTH, "focal",
             "26 months, and valid until revoked", "in"),
            ("Partner token", "OAuth · cert-bound", 15, "backend",
             "15 min: would have expired before the revocation", "out"),
            ("Workload SVID", "SPIRE · renewed at 30 min", HOUR, "backend", "1 h", "out"),
            ("Break-glass session", "two people", HOUR, "backend", "60 min, posted and reviewed", "out")]
    for i, (name, sub, life, kind, note, where) in enumerate(rows):
        y = p.y + 12 + i * 48
        x0, x1 = p.px(0), p.px(log10(life))
        d.nodes.append(f'<rect class="dg-n dg-n-{kind}" x="{x0:.1f}" y="{y}" width="{x1 - x0:.1f}" height="24" rx="3"/>')
        d.extra.append(f'<text class="dg-name" x="104" y="{y + 10}">{name}</text>'
                       f'<text class="dg-sub" x="104" y="{y + 23}">{sub}</text>')
        if where == "in":
            d.note(int(x1 - 8), y + 16, note, anchor="end")
        else:
            d.note(int(max(x1, xr) + 8), y + 16, note)
    d.legend([("focal", "Static secret"), ("backend", "Short-lived credential")])
    return d
