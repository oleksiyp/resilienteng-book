"""Figure 4.5: Encore's delivery rings, widening by population."""
from dg import Diagram
from registry import figure


@figure
def fig_4_5():
    d = Diagram("fig-4-5", 864, 436, "Encore's delivery rings",
                "Four concentric rings: staff and synthetic buyers at the centre, then the pooled self-service "
                "cells, then the Professional cells, then Encore's own fan site and the Enterprise silo for "
                "venue-chain-a, which its contract places last. A change widens outward one ring at a time.")
    CX, BY = 432, 344
    radii = [80, 150, 220, 290]

    def semi(r):
        return f"M {CX - r},{BY} A {r},{r} 0 0 1 {CX + r},{BY} Z"

    for r in reversed(radii[1:]):
        d.zones.append(f'<path class="dg-ill-fill" d="{semi(r)}"/>')
    d.zones.append(f'<path class="dg-ill-fill-accent" d="{semi(radii[0])}"/>')
    d.zones.append(f'<line class="dg-ill-ink" x1="{CX - 312}" y1="{BY}" x2="{CX + 312}" y2="{BY}"/>')
    rings = [(BY - 30, "Staff", "and synthetic buyers"),
             (BY - 106, "Self-service cells", "~500 venues, cells of ~50"),
             (BY - 176, "Professional cells", "Kubernetes, database per tenant"),
             (BY - 246, "Fan site & venue-chain-a", "Enterprise silo: last, by contract")]
    for y, name, sub in rings:
        d.extra.append(f'<text class="dg-name" x="{CX}" y="{y}">{name.replace("&", "&amp;")}</text>')
        d.extra.append(f'<text class="dg-sub" x="{CX}" y="{y + 14}">{sub}</text>')
    d.path([(CX + 88, BY + 24), (CX + 288, BY + 24)], label="EXPOSURE WIDENS, RING BY RING", side="below")
    d.note(CX - 300, BY + 36, "each ring waits for the evidence of the last")
    d.legend([("focal", "First ring: those who chose to be early"), ("backend", "Later rings"),
              ("arrow:muted", "Order of exposure")])
    return d
