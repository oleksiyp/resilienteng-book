"""Figure 6.6: the October region failover game day, EU-1 isolated, EU-2 takes over with the EU-3 witness."""
from dg import Diagram
from registry import figure


@figure
def fig_6_6():
    d = Diagram("fig-6-6", 864, 640, "The region failover game day",
                "EU-1 is isolated from EU-2 and from the witness in EU-3, and every event homed there fails over "
                "to EU-2. The core held: the EU-1 seat-ledger leaders lost their majority and stopped writing, "
                "leaders were re-elected in EU-2 with the EU-3 witness's votes, fencing rejected late writes from "
                "the deposed leaders, and the failover took about four minutes end to end. Three edges did not: "
                "the Sale Gate was pre-warmed only in EU-1, Bot Screening's risk data reached EU-2 only by a daily "
                "copy, and an Orders reconciliation job whose schedule named EU-1 sat idle for six hours.")
    W, H = 200, 56
    A, B = 40, 624
    R = [136, 224, 312, 400]
    d.zone(16, 112, 248, 376, "EU-1 · ISOLATED")
    d.zone(600, 112, 248, 376, "EU-2 · TAKES OVER")
    d.zone(312, 504, 240, 88, "EU-3 · WITNESS")
    # traffic
    d.path([(392, 88), (392, 164), (A + W, 164)], dashed=True, label="BEFORE", at=1, side="above")
    d.path([(472, 88), (472, 164), (B, 164)], label="AFTER", at=1, side="above")
    # seat ledger
    d.path([(A + W, 240), (B, 240)], dashed=True, label="REPLICATION · LINK CUT")
    d.path([(A + W, 264), (B, 264)], kind="accent", dashed=True, label="LATE WRITES · FENCED, REJECTED",
           side="below")
    d.path([(552, 548), (584, 548), (584, 296), (680, 296), (680, 280)], label="VOTES", at=1, side="left")
    # risk data
    d.path([(A + W, 340), (B, 340)], dashed=True, label="DAILY COPY ONLY")
    # nodes
    d.node(332, 32, 200, 56, "Fans + synthetic buyers", "small events · test event", "input")
    d.node(A, R[0], W, H, "Sale Gate", "pre-warmed here")
    d.node(A, R[1], W, H, "Seat Inventory", "leaders lose majority")
    d.node(A, R[2], W, H, "Risk data", "Bot Screening account", "store")
    d.node(A, R[3], W, H, "Orders reconciliation", "schedule names EU-1")
    d.node(B, R[0], W, H, "Sale Gate", "cold starts", "optional")
    d.node(B, R[1], W, H, "Seat Inventory", "re-elected · ~4 min end to end")
    d.node(B, R[2], W, H, "Risk data", "yesterday's signals", "optional")
    d.node(B, R[3], W, H, "Orders reconciliation", "idle for 6 h", "optional")
    d.node(336, 520, 192, 56, "Seat ledger witness", "holds the log, votes", "store")
    d.note(424, 424, "no hold or sale lost; each finding", anchor="middle")
    d.note(424, 438, "became a ticket with an owner", anchor="middle")
    d.legend([("backend", "Held"), ("optional", "Found at the edges"), ("arrow:muted", "Traffic, votes"),
              ("arrow:muted:dashed", "Before, cut or copied daily"), ("arrow:accent:dashed", "Fenced write")])
    return d
