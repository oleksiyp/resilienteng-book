"""Figure 8.6 — the degradation ladder and what pulls it."""
from dg import Diagram
from registry import figure


@figure
def fig_8_6():
    d = Diagram("fig-8-6", 864, 384, "The degradation ladder",
                "Four rungs stepping down from the normal state, frontier and cheap tiers, to a pinned fallback "
                "provider, to retrieval only, to human handoff. The gateway's circuit breakers, tripped by errors, "
                "latency or rate-limit exhaustion, pull the ladder to the fallback automatically; a sustained burn of "
                "the refund-explanation quality SLI pages the on-call engineer, who may flip a prepared switch that "
                "drops refund intents to retrieval only, because a model that is available but wrong never trips a "
                "breaker and a noisy judge-based signal is not trusted to act alone.")
    W, H = 192, 56
    xs = [24, 232, 440, 648]
    ys = [40, 88, 136, 184]
    for i in range(3):
        d.path([(xs[i] + W, ys[i] + 28), (xs[i + 1] + 40, ys[i] + 28), (xs[i + 1] + 40, ys[i + 1])])
    d.path([(328, 264), (328, ys[1] + H)], label="TRIPS", side="right")
    d.path([(536, 264), (536, ys[2] + H)], kind="accent", label="ON-CALL SWITCH", side="right")
    rungs = [("Frontier + cheap", "generated, cited answers", "RUNG 1 · NORMAL"),
             ("Fallback provider", "same job, other model", "RUNG 2"),
             ("Retrieval only", "help articles, order status", "RUNG 3"),
             ("Human handoff", "queue, summary, honest wait", "RUNG 4")]
    for (name, sub, tag), x, y in zip(rungs, xs, ys):
        d.node(x, y, W, H, name, sub, "focal" if tag.startswith("RUNG 1") else "backend", tag=tag)
    d.node(232, 264, W, H, "Gateway breakers", "errors · latency · rate limit", "input")
    d.node(440, 264, W, H, "Refund quality SLI", "burn pages on-call", "input")
    d.note(448, 64, "EVERY RUNG DECIDED IN ADVANCE")
    d.note(448, 78, "AND EXERCISED ON GAME DAYS")
    d.legend([("backend", "Rung: what the fan gets"), ("input", "Trigger"),
              ("arrow:muted", "Steps down"), ("arrow:accent", "The trigger teams forget")])
    return d
