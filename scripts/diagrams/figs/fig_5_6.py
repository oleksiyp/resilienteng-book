"""Figure 5.6: shuffle sharding in a self-service cell, eight lanes and two per venue."""
from dg import Diagram
from registry import figure


@figure
def fig_5_6():
    d = Diagram("fig-5-6", 864, 412, "Shuffle sharding in a cell",
                "Eight worker lanes in one self-service cell, with each venue assigned two. Venue A's runaway "
                "import floods lanes 2 and 5. Venues B and C share one flooded lane each, and their consumers move "
                "the work to their other lane; D and E share none; F, by chance, holds the same pair and is hit. "
                "Any one neighbor has about a 1-in-28 chance of that, so in a cell of 50 one or two are hit.")
    LX, LW, Y0, RS = 216, 52, 72, 40
    lane = lambda k: LX + (k - 1) * LW + LW // 2  # noqa: E731
    flooded = (2, 5)
    rows = [("Venue A", "focal", (2, 5), "runaway import floods both"),
            ("Venue B", "input", (2, 7), "work moves to L7"),
            ("Venue C", "input", (1, 5), "work moves to L1"),
            ("Venue D", "input", (3, 8), "untouched"),
            ("Venue E", "input", (4, 6), "untouched"),
            ("Venue F", "input", (2, 5), "same pair: hit")]
    bottom = Y0 + len(rows) * RS
    shade = " ".join(f"M {lane(k) - 20},{Y0 - 8} h 40 v {bottom - Y0 + 4} h -40 z" for k in flooded)
    d.zones.append(f'<path class="dg-ill-fill-accent" d="{shade}"/>')
    for k in range(1, 9):
        d.zones.append(f'<line class="dg-ill-soft" x1="{lane(k)}" y1="{Y0 - 8}" x2="{lane(k)}" y2="{bottom - 4}"/>')
        d.note(lane(k), 52, f"L{k}", anchor="middle")
    for r, (name, kind, lanes, outcome) in enumerate(rows):
        y = Y0 + r * RS
        d.node(24, y, 144, 32, name, None, kind)
        a, b = (lane(k) for k in lanes)
        d.extra.append(f'<line class="dg-ill-ink" x1="{a}" y1="{y + 16}" x2="{b}" y2="{y + 16}"/>')
        for k in lanes:
            d.extra.append(f'<circle class="dg-ill-fill" cx="{lane(k)}" cy="{y + 16}" r="7"/>')
        d.note(LX + 8 * LW + 16, y + 20, outcome)
    d.note(24, bottom + 32, "Fixed partitions (four groups of two lanes): a runaway venue takes its whole group, about")
    d.note(24, bottom + 48, "12 of its 49 neighbors. Shuffled pairs (28): one or two share both lanes, if work can move.")
    d.legend([("focal", "Noisy venue and its flooded lanes"), ("input", "Neighbor venue"),
              ("backend", "Lane assigned to a venue")])
    return d
