"""Figure 7.4: the spring XML-parser CVE, images fixed against hours since disclosure."""
from dg import Diagram
from chartkit import Plot
from registry import figure


@figure
def fig_7_4():
    d = Diagram("fig-7-4", 864, 304, "Patching a known-exploited flaw in 48 hours",
                "Images redeployed against hours since disclosure. SBOM queries found 37 affected images in 20 "
                "minutes; a WAF rule went up within 6 hours; 35 images were redeployed by hour 30 and all 37 of "
                "Encore's own by hour 48, the deadline. The vendor's monitoring agent, confined by an egress rule, "
                "was fixed four days later.")
    p = Plot(d, x=72, y=48, w=744, h=208, xr=(0, 150), yr=(0, 40))
    p.axes(xticks=[0, 24, 48, 72, 96, 120, 144], yticks=[0, 10, 20, 30, 37],
           xfmt=lambda t: f"{t} H", xlabel="HOURS SINCE DISCLOSURE", ylabel="AFFECTED IMAGES REDEPLOYED")
    p.band(48, 144, kind="soft")
    d.label_at("VENDOR TAIL · AGENT CONFINED BY AN EGRESS RULE", p.px(96), p.py(18), horizontal=True, side="below")
    p.vline(6, label="WAF RULE · 6 H", kind="soft", at=0.04)
    p.vline(48, label="48 H DEADLINE", kind="accent", dashed=True, at=0.5)
    p.line([(0, 0), (30, 35), (48, 37), (144, 37)], kind="ink")
    p.dot(30, 35, kind="ink")
    p.dot(48, 37, kind="ink")
    p.dot(144, 38, kind="accent")
    p.annotate(10, 3, "20 MIN: SBOMS LOCATE 37 IMAGES", dx=0, dy=0)
    p.annotate(30, 35, "35 BY HOUR 30", dx=4, dy=16)
    p.annotate(48, 37, "ALL 37 OF ENCORE'S OWN", dx=8, dy=-8)
    p.annotate(144, 38, "VENDOR AGENT · 4 DAYS LATER", dx=-8, dy=-8, anchor="end")
    return d
