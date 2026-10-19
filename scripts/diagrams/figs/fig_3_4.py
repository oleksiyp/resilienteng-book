"""Figure 3.4: Kubernetes upgrades in waves across Encore's 14 clusters."""
from dg import Diagram
from registry import figure


@figure
def fig_3_4():
    d = Diagram("fig-3-4", 864, 316, "Upgrade waves across 14 clusters",
                "Each of the two regions, EU-1 and EU-2, runs a core cluster and six Professional cells. "
                "A new Kubernetes version reaches the canary cell of internal test tenants in EU-1 first, "
                "then the other eleven cells a few at a time, then the two core clusters, with node pools "
                "drained through PodDisruptionBudgets and a scan for removed APIs before each wave.")
    R1, R2, H = 80, 152, 48
    # zones
    d.zone(72, 52, 168, 176, "WAVE 1")
    d.zone(272, 52, 344, 176, "WAVE 2 · A FEW CELLS AT A TIME")
    d.zone(648, 52, 192, 176, "WAVE 3")
    # connectors between waves
    d.path([(240, 140), (272, 140)])
    d.path([(616, 140), (648, 140)])
    # region labels
    d.note(24, R1 + 28, "EU-1")
    d.note(24, R2 + 28, "EU-2")
    # nodes
    d.node(88, R1, 136, H, "Canary cell", "internal test tenants", "focal")
    for i in range(1, 6):   # EU-1's first cell is the canary
        d.node(280 + i * 56, R1, 48, H, f"C{i + 1}", "cell")
    for i in range(6):
        d.node(280 + i * 56, R2, 48, H, f"C{i + 1}", "cell")
    d.node(664, R1, 160, H, "Core EU-1", "Encore's services")
    d.node(664, R2, 160, H, "Core EU-2", "Encore's services")
    d.note(432, 256, "Before every wave: scan manifests for APIs the new version removes. "
                     "Within a wave: the reconciler drains nodes through PDBs.", anchor="middle")
    d.legend([("focal", "Canary cell"), ("backend", "Professional cell or core cluster"),
              ("arrow:muted", "Next wave, once the last one is healthy")])
    return d
