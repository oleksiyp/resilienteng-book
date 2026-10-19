"""Figure 5.1: the AT&T cascade of 15 January 1990, and the recovery loop that sustained it."""
import random

from dg import Diagram
from registry import figure


@figure
def fig_5_1():
    d = Diagram("fig-5-1", 864, 476, "The AT&T cascade, 1990",
                "Left: a map of switches joined to their neighbors, with the first switch, in New York, at the "
                "centre and the waves of resets spreading outward from it. Right: the loop each switch ran. "
                "A switch recovers and tells its neighbors it is back in service; a neighbor that receives a "
                "second message while still handling the first hits the defect, corrupts its data and resets; "
                "when it recovers, it becomes the next sender.")
    OX, OY = 224, 224
    rnd = random.Random(11)
    pos = {}
    for i in range(7):
        for j in range(6):
            if (i, j) == (3, 3):
                pos[i, j] = (OX, OY)
            else:
                pos[i, j] = (56 + 56 * i + rnd.randint(-12, 12), 56 + 56 * j + rnd.randint(-12, 12))
    links = []
    for (i, j), (x, y) in pos.items():
        for di, dj in ((1, 0), (0, 1), (1, 1)):
            n = (i + di, j + dj)
            if n in pos and (di + dj == 1 or rnd.random() < 0.3):
                x2, y2 = pos[n]
                links.append(f'<line class="dg-ill-soft" x1="{x}" y1="{y}" x2="{x2}" y2="{y2}"/>')
    d.zones.append("\n".join(links))
    for k, r in enumerate((60, 116, 172)):
        d.zones.append(f'<circle class="dg-ill-soft" cx="{OX}" cy="{OY}" r="{r}" stroke-dasharray="5 4"/>')
        d.label_at(f"WAVE {k + 1}", OX, OY + r, horizontal=True, side="below")
        d.extra.append(d.labels.pop())  # on top of the switches
    for (i, j), (x, y) in pos.items():
        if (i, j) != (3, 3):
            d.nodes.append(f'<circle class="dg-ill-fill" cx="{x}" cy="{y}" r="6"/>')
    d.nodes.append(f'<circle class="dg-ill-fill-accent" cx="{OX}" cy="{OY}" r="9"/>')
    d.label_at("NEW YORK · MINOR FAULT", OX, OY - 6, horizontal=True, side="above")
    d.extra.append(d.labels.pop())
    # the loop each switch runs
    d.start(616, 40)
    d.path([(616, 46), (616, 72)])
    d.path([(616, 128), (616, 168), (656, 168)])
    d.note(608, 152, "\"back in service\"", anchor="end")
    d.path([(752, 196), (752, 232)])
    d.path([(656, 260), (616, 260), (616, 288)])
    d.path([(536, 316), (488, 316), (488, 100), (536, 100)], kind="accent",
           label="IT IS NOW THE SENDER", at=1, side="right")
    d.state(536, 72, 160, 56, "Switch recovers", "returns to service")
    d.state(656, 140, 184, 56, "Neighbors get messages", "a second while busy")
    d.state(656, 232, 184, 56, "Defect fires", "break exits too early")
    d.state(536, 288, 160, 56, "Neighbor resets", "data corrupted")
    d.note(632, 44, "trigger: one switch, one minor fault")
    d.note(472, 380, "The trigger lasted seconds; the loop ran for about nine hours.")
    d.note(472, 396, "All 114 switches ran the same code, so redundancy could not help.")
    d.legend([("focal", "The first switch"), ("backend", "Switch or step"),
              ("arrow:accent", "The recovery loop that sustained the outage")])
    return d
