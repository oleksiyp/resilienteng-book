"""Figure 8.4 — the request path through the AI gateway, and the eval loop beside it."""
from dg import Diagram
from registry import figure


@figure
def fig_8_4():
    d = Diagram("fig-8-4", 864, 560, "The AI request path and its eval loop",
                "Fans reach the support assistant and the refund agent, which call models only through the AI "
                "gateway; the gateway sends about 80% of turns to the cheap tier, hard turns to the frontier tier "
                "and fails over to a second provider. The refund agent gets a 15-minute token by token exchange, "
                "calls tools through the MCP server and the refund workflow, which sends some refunds to a human "
                "review queue. Beside the path, a 3% daily sample of conversations and the nightly golden set "
                "pass through the same evaluators, whose quality SLI pages the on-call engineer who can pull the "
                "gateway's degradation ladder, and production failures become new golden cases.")
    H = 56
    # --- request path
    d.path([(152, 124), (176, 124), (176, 68), (200, 68)])
    d.path([(152, 124), (176, 124), (176, 168), (200, 168)])
    d.path([(384, 68), (416, 68)])
    d.path([(384, 180), (416, 180)])
    d.path([(568, 64), (616, 64)], label="≈80%")
    d.path([(568, 124), (616, 124)])
    d.path([(568, 184), (616, 184)], dashed=True)
    # identity and tools
    d.path([(100, 264), (100, 196), (200, 196)], label="15-MIN TOKEN", at=0, side="right", kind="link")
    d.path([(292, 208), (292, 264)], label="TOOL CALLS", side="right")
    d.path([(292, 320), (292, 352)])
    d.path([(292, 408), (292, 440)], label="OUTSIDE AUTO RULE", side="right")
    # --- eval loop
    d.path([(520, 208), (520, 292), (616, 292)], label="CONVERSATIONS", at=1, side="above")
    d.path([(728, 320), (728, 352)], label="3% DAILY", side="right")
    d.path([(728, 440), (728, 408)], label="NIGHTLY", side="right")
    d.path([(616, 380), (472, 380), (472, 208)], kind="link", label="SLI 98% · PAGES", at=0, side="above")
    d.path([(840, 396), (848, 396), (848, 468), (840, 468)], kind="accent", label=None)
    d.label_at("NEW CASES", 848, 432, horizontal=False, side="left", kind="accent")
    # --- nodes
    d.node(24, 96, 128, H, "Fan", "chat, ticket", "input")
    d.node(200, 40, 184, H, "Support assistant", "RAG over help, orders")
    d.node(200, 152, 184, H, "Refund agent", "acts for one fan")
    d.node(416, 40, 152, 168, "AI gateway", "route · meter · break", "focal")
    d.node(616, 40, 224, 48, "Cheap tier", "pinned snapshot", "external")
    d.node(616, 100, 224, 48, "Frontier tier", "hard turns", "external")
    d.node(616, 160, 224, 48, "Fallback provider", "pinned, tested weekly", "optional")
    d.node(24, 264, 152, H, "Token exchange", "RFC 8693", "store")
    d.node(200, 264, 184, H, "MCP server", "orders:read · refunds:request")
    d.node(200, 352, 184, H, "Refund workflow", "€80 and 48 h, in code")
    d.node(200, 440, 184, H, "Human review queue", "policy panel, seeded", "input")
    d.node(616, 264, 224, H, "Production sample", "3% a day · 40 a week to people", "store")
    d.node(616, 352, 224, H, "Evaluators", "calibrated judges · code checks", "focal")
    d.node(616, 440, 224, H, "Golden set", "200 cases · each run five times", "store")
    d.legend([("input", "People"), ("focal", "Control point"), ("external", "Provider"),
              ("arrow:muted", "Request or call"), ("arrow:link", "Token or signal"),
              ("arrow:accent", "Failures feed the set")])
    return d
