"""Figure 6.2: RPO and RTO as claims, against what the Finance ledger drills measured."""
from dg import Diagram
from chartkit import Plot
from registry import figure


@figure
def fig_6_2():
    d = Diagram("fig-6-2", 864, 360, "RPO and RTO around a failure, promised and measured",
                "A time axis in hours around a failure at zero. The seat ledger promises an RPO of zero and an RTO "
                "of minutes. The Finance ledger promises 15 minutes of data loss and two hours to restore; its "
                "spring drill took about nine hours, and the second drill had the current year writable in "
                "1 h 50 min, with history following within a day.")
    p = Plot(d, x=200, y=56, w=640, h=208, xr=(-1, 10), yr=(0, 4))
    p.axes(xticks=[-1, 0, 2, 4, 6, 8, 10], xfmt=lambda t: "FAILURE" if t == 0 else f"{t:+d} H",
           xlabel="HOURS FROM THE FAILURE", grid=False)
    # failure line and the promised 2 h RTO
    p.vline(0, kind="ink", dashed=False)
    p.vline(2, kind="soft", dashed=True)
    d.label_at("PROMISED RTO · 2 H", p.px(2), p.y - 4, horizontal=True, side="above")
    d.label_at("LAST GOOD COPY ← RPO · RTO → SERVICE BACK", p.px(0), p.y - 22, horizontal=True, side="above")

    rows = [("Seat ledger", "promised"), ("Finance ledger", "promised"),
            ("Finance, drill 1", "spring · 4.2 TB"), ("Finance, drill 2", "current year first")]
    BH = 24
    ys = [p.y + 16 + i * 52 for i in range(4)]

    def bar(y, a, b, kind, dash=False):
        x0, x1 = p.px(a), p.px(b)
        da = ' stroke-dasharray="4,3"' if dash else ""
        d.nodes.append(f'<rect class="dg-n dg-n-{kind}" x="{x0:.1f}" y="{y}" width="{x1 - x0:.1f}" '
                       f'height="{BH}" rx="3"{da}/>')

    for (name, sub), y in zip(rows, ys):
        d.extra.append(f'<text class="dg-name" x="104" y="{y + 10}">{name}</text>'
                       f'<text class="dg-sub" x="104" y="{y + 23}">{sub}</text>')
    # seat ledger: RPO 0, RTO minutes (election and re-routing took about 4 min at the game day)
    bar(ys[0], 0, 4 / 60, "backend")
    d.note(int(p.px(2.2)), ys[0] + 16, "RPO 0 (majority commit) · RTO minutes")
    # Finance promise
    bar(ys[1], -0.25, 0, "store")
    bar(ys[1], 0, 2, "backend")
    d.note(int(p.px(2.2)), ys[1] + 16, "RPO 15 min · RTO 2 h")
    # drill 1: ~9 h
    bar(ys[2], 0, 9, "focal")
    d.note(int(p.px(9) - 8), ys[2] + 16, "~9 h: approvals, I/O, verification", anchor="end")
    # drill 2: current year writable in 1 h 50 min; history within a day
    bar(ys[3], 0, 110 / 60, "backend")
    bar(ys[3], 110 / 60, 10, "optional", dash=True)
    d.note(int(p.px(2.2)), ys[3] + 16, "1 h 50 min · history follows, within a day →")
    d.legend([("store", "RPO: data lost"), ("backend", "RTO: time to restore"),
              ("focal", "Missed the promise"), ("optional", "Restored later, by agreement")])
    return d
