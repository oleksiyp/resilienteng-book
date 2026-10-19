"""Figure 5.3: retry amplification across layers, against a retry budget."""
from chartkit import Plot
from dg import Diagram
from registry import figure


def attempts(p, retries):
    """Expected calls made by one layer that retries `retries` times, each failing with probability p."""
    return sum(p ** k for k in range(retries + 1))


def stacked(p, layers, retries):
    load, fail = 1.0, p
    for _ in range(layers):
        load *= attempts(fail, retries)
        fail = fail ** (retries + 1)
    return load


@figure
def fig_5_3():
    d = Diagram("fig-5-3", 864, 388, "Retries multiply across layers",
                "Load on a struggling dependency, as a multiple of normal, against the share of its calls that "
                "fail. One layer retrying three times can at most quadruple the load; three such layers stacked "
                "can multiply it 64 times as failure approaches 100%; a 10% retry budget caps it at 1.1 times.")
    p = Plot(d, x=72, y=48, w=744, h=240, xr=(0, 1), yr=(1, 64), ylog=True)
    p.axes(xticks=[0, .25, .5, .75, 1], yticks=[1, 2, 4, 16, 64],
           xlabel="SHARE OF CALLS TO THE DEPENDENCY THAT FAIL", ylabel="LOAD ON THE DEPENDENCY (× NORMAL, LOG)",
           xfmt=lambda t: f"{t:.0%}", yfmt=lambda t: f"{t:g}×")
    xs = [i / 200 for i in range(201)]
    p.line([(x, stacked(x, 3, 3)) for x in xs], kind="accent")
    p.line([(x, attempts(x, 3)) for x in xs], kind="soft")
    p.line([(x, 1 + min(x, 0.1)) for x in xs], kind="ink")
    p.annotate(1, 64, "3 LAYERS × 3 RETRIES: 64×", dx=-8, dy=12, kind="accent", anchor="end")
    p.annotate(1, 4, "1 LAYER × 3 RETRIES: 4×", dx=-8, dy=-8, anchor="end")
    p.annotate(1, 1.1, "10% RETRY BUDGET: 1.1×", dx=-8, dy=-8, anchor="end")
    d.legend([("arrow:accent", "Three layers, three retries each"), ("arrow:muted", "One layer, three retries"),
              ("arrow:muted", "One layer, 10% budget")])
    return d
