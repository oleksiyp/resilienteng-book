"""Figure 1.1 — Encore's system map: people, the edge, the services, the stream and the outside parties."""
from dg import Diagram
from registry import figure


@figure
def fig_1_1():
    d = Diagram("fig-1-1", 864, 596, "Encore's system map",
                "Fans, organizers, partners and tenants enter through the API gateway. The purchase path runs "
                "from the Sale Gate through Bot Screening and Seat Inventory to Orders & Payments and the "
                "external payment providers, two of them. Catalog uses a bought search product; Support uses the AI gateway "
                "to reach model providers and asks Orders for refunds. Seat Inventory and Orders publish to "
                "the ticket-sales.v2 stream, which Notifications, the Finance ledger and Sales Analytics consume.")
    T, H = 56, 56
    rows = [T, T + 88, T + 176, T + 264]          # 56, 144, 232, 320
    P, GX, A, B, C = 24, 192, 336, 520, 704
    # connectors first
    for y in rows:                                 # people enter at the edge
        d.path([(P + 128, y + 28), (GX, y + 28)])
    d.path([(244, T), (244, 36), (596, 36), (596, T)], label="BROWSE, SEARCH, SEAT MAPS", at=1)
    d.path([(GX + 104, T + 28), (412, T + 28), (412, rows[3])], kind="accent")   # the purchase path
    d.path([(A + 152, rows[3] + 28), (B, rows[3] + 28)], kind="accent")
    d.path([(B + 152, T + 28), (C, T + 28)])
    d.path([(B + 152, rows[1] + 28), (C, rows[1] + 28)])
    d.path([(772, rows[1] + H), (772, rows[2])])
    d.path([(560, rows[1] + H), (560, 304), (464, 304), (464, rows[3])], label="REFUNDS", at=0, side="right")
    d.path([(A, rows[2] + 28), (320, rows[2] + 28), (320, 416)], dashed=True)
    d.path([(412, rows[3] + H), (412, 416)], dashed=True)
    for cx in (412, 596, 772):
        d.path([(cx, 456), (cx, 492)], dashed=True)
    # people
    d.node(P, rows[0], 128, H, "Fans", "queue, seats, wallet", "input")
    d.node(P, rows[1], 128, H, "Organizers", "events, payouts", "input")
    d.node(P, rows[2], 128, H, "Partners", "venues, resale apps", "input")
    d.node(P, rows[3], 128, H, "Tenants", "venues on SaaS cells", "input")
    # the edge
    d.node(GX, T, 104, 320, "API gateway", "api.encore.com")
    # services
    d.node(A, rows[0], 152, H, "Sale Gate", "waiting room, admission")
    d.node(A, rows[1], 152, H, "Bot Screening", "rented edge signals")
    d.node(A, rows[2], 152, H, "Seat Inventory", "4 shards, 5-min holds", "store")
    d.node(A, rows[3], 152, H, "Orders & Payments", "purchase saga, 3 s")
    d.node(B, rows[0], 152, H, "Catalog", "events, seat geometry")
    d.node(B, rows[1], 152, H, "Support", "assistant, refund agent")
    d.node(B, rows[3], 152, H, "PSPs", "two; cards, ~800 ms", "external")
    d.node(C, rows[0], 136, H, "Search", "a bought product", "external")
    d.node(C, rows[1], 136, H, "AI gateway", "routes model turns")
    d.node(C, rows[2], 136, H, "Model providers", "frontier, cheap tier", "external")
    d.node(312, 416, 528, 40, "ticket-sales.v2",
           "SeatReserved · SeatSold · TicketIssued · SaleCompleted", "store")
    d.node(A, 492, 152, 52, "Notifications", "email, wallet passes")
    d.node(B, 492, 152, 52, "Finance ledger", "daily reconcile", "store")
    d.node(C, 492, 136, 52, "Sales Analytics", "a consumer only")
    d.legend([("input", "People"), ("backend", "Encore service"), ("store", "Holds the record"),
              ("external", "Bought or outside"), ("arrow:accent", "Purchase path"),
              ("arrow:muted:dashed", "Event, not a call")])
    return d
