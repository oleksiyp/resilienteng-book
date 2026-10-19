"""Figure 6.4: fencing tokens stop a deposed leader at the storage."""
from dg import Diagram
from registry import figure
from seqkit import actor, lifeline, activation, message

OLD, STORE, NEW = 120, 432, 744


@figure
def fig_6_4():
    d = Diagram("fig-6-4", 864, 432, "Fencing a deposed leader",
                "The old leader of a Seat Inventory shard writes with term 7 and is accepted. It is then paused or "
                "cut off. The new leader records term 8 at the storage and writes with it. When the old leader "
                "wakes and writes with term 7, the storage rejects the write as stale, and the old leader learns "
                "only then that it was replaced.")
    for cx in (OLD, STORE, NEW):
        lifeline(d, cx, 76, 372)
    activation(d, STORE, 104, 356)
    message(d, OLD, STORE, 120, "WRITE HOLD · TERM 7 · OK")
    message(d, NEW, STORE, 200, "RECORD TERM 8")
    message(d, NEW, STORE, 248, "WRITE HOLD · TERM 8 · OK")
    message(d, OLD, STORE, 296, "WRITE HOLD · TERM 7", kind="accent")
    message(d, STORE, OLD, 336, "REJECTED · STALE TERM", kind="accent", dashed=True)
    actor(d, OLD, 168, "Old leader", "holds term 7", "backend")
    actor(d, STORE, 168, "Shard storage", "newest term seen", "store")
    actor(d, NEW, 168, "New leader", "elected, term 8", "backend")
    d.state(56, 148, 128, 120, "Paused", "GC or partition", "optional")
    d.note(STORE + 12, 222, "newest term: 8")
    d.note(OLD + 12, 360, "it learns of its replacement only here")
    d.legend([("backend", "Leader"), ("store", "Storage that enforces terms"),
              ("arrow:muted", "Accepted"), ("arrow:accent", "Stale write, rejected")])
    return d
