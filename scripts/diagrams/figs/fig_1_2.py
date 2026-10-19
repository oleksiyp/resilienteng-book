"""Figure 1.2 — one fan's purchase on an on-sale morning, as eight numbered steps."""
from dg import Diagram
from registry import figure


@figure
def fig_1_2():
    d = Diagram("fig-1-2", 864, 376, "One fan's purchase, step by step",
                "Eight steps in two rows. The fan waits in the Sale Gate's room, is admitted at no more than about "
                "1,200 fans a second per event, passes Bot Screening, sees a seat map whose geometry comes from "
                "Catalog's cache and whose availability comes from Seat Inventory, holds seats for five minutes "
                "with POST /holds, completes a checkout saga within a 3-second budget of which about 800 ms is the "
                "payment provider, after which SeatSold and TicketIssued are published and Notifications delivers "
                "the ticket to the fan's wallet.")
    W, H = 180, 72
    xs = [24, 236, 448, 660]
    R1, R2 = 56, 216
    d.extra.append('<text class="dg-eyebrow" x="24" y="36" style="text-anchor:start">'
                   'ONE FAN, ON-SALE MORNING · READ ALONG THE ARROWS</text>')
    # connectors
    for a, b in zip(xs, xs[1:]):
        d.path([(a + W, R1 + 36), (b, R1 + 36)])
    d.path([(824, R1 + H), (824, R2)])
    for a, b in zip(xs[::-1], xs[::-1][1:]):
        d.path([(a, R2 + 36), (b + W, R2 + 36)])
    steps = [
        (xs[0], R1, "1 · SALE GATE", "Wait in the room", "queue position, in order", "backend",
         "minutes, sometimes an hour;", "the room absorbs the 500×"),
        (xs[1], R1, "2 · SALE GATE", "Admitted", "≤ ~1,200 fans/s per event", "focal",
         "the dial that keeps every", "shard under 80% load"),
        (xs[2], R1, "3 · BOT SCREENING", "Screened", "edge signals, velocity rules", "backend",
         "the bots arrive first;", "real fans must pass"),
        (xs[3], R1, "4 · CATALOG + SEAT INVENTORY", "Seat map", "shape cached, seats live", "backend",
         "geometry: Catalog's cache", "availability: Inventory"),
        (xs[3], R2, "5 · SEAT INVENTORY", "Hold", "POST /holds · 5-min TTL", "backend",
         "on one of four shards, in", "the event's home region"),
        (xs[2], R2, "6 · ORDERS & PAYMENTS", "Checkout saga", "3 s budget, ~800 ms at PSP", "focal",
         "Idempotency-Key on the buy;", "PSP down: the second PSP"),
        (xs[1], R2, "7 · TICKET-SALES.V2", "Facts published", "SeatSold, TicketIssued", "backend",
         "SaleCompleted feeds", "Finance and Analytics"),
        (xs[0], R2, "8 · NOTIFICATIONS", "Ticket in the wallet", "email and wallet pass", "backend",
         "one ticket, delivered once:", "the rewrite's lesson"),
    ]
    for x, y, tag, name, sub, kind, n1, n2 in steps:
        d.node(x, y, W, H, name, sub, kind, tag=tag)
        d.note(x + 4, y + H + 20, n1)
        d.note(x + 4, y + H + 33, n2)
    d.legend([("backend", "Step, tagged with the service that owns it"),
              ("focal", "The two numbers that bound the rush"), ("arrow:muted", "The fan moves on")])
    return d
