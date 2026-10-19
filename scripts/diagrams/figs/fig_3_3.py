"""Figure 3.3: governors in a hierarchy, each slower loop setting a faster loop's set point."""
from dg import Diagram
from registry import figure


@figure
def fig_3_3():
    d = Diagram("fig-3-3", 864, 592, "Governors in a hierarchy",
                "Argo CD pulls Catalog's desired state from the encore-deploy repository and writes the "
                "autoscaler's floor and CPU target; the autoscaler, watching pod CPU, writes spec.replicas; "
                "the Deployment controller creates pods; pending pods prompt the cluster autoscaler to add "
                "nodes, while the node-upgrade reconciler drains nodes through PodDisruptionBudgets. "
                "A manual kubectl scale writes spec.replicas as a second owner and leaves no record; "
                "a planned surge instead raises the autoscaler's floor in Git.")
    H = 56
    CX, CW = 304, 224          # loop column
    MID = CX + CW // 2         # 416
    rows = [48, 152, 256, 360, 464]
    # connectors
    d.path([(216, rows[0] + 28), (CX, rows[0] + 28)], label="PULLS")
    d.path([(MID, rows[0] + H), (MID, rows[1])], label="MINREPLICAS · CPU TARGET", side="right")
    d.path([(MID, rows[1] + H), (MID, rows[2])], label="SPEC.REPLICAS", side="right")
    d.path([(MID, rows[2] + H), (MID, rows[3])], label="CREATES PODS", side="right")
    d.path([(CX, rows[3] + 28), (264, rows[3] + 28), (264, rows[1] + 28), (CX, rows[1] + 28)],
           kind="link", dashed=True, label="CPU", at=1, side="left")
    d.path([(CX + CW, rows[3] + 28), (624, rows[3] + 28)], label="PENDING")
    d.path([(720, rows[3] + H), (720, rows[4] + 28), (CX + CW, rows[4] + 28)], label="ADDS NODES", at=1)
    d.path([(216, rows[4] + 28), (CX, rows[4] + 28)], label="DRAINS · PDB")
    d.path([(624, rows[2] + 28), (CX + CW, rows[2] + 28)], kind="accent", dashed=True, label="NO RECORD")
    # nodes
    d.node(24, rows[0], 192, H, "encore-deploy", "desired state in Git", "store")
    d.node(CX, rows[0], CW, H, "Argo CD", "GitOps agent · every ~3 min")
    d.node(CX, rows[1], CW, H, "Horizontal Pod Autoscaler", "15 s up · 5 min down")
    d.node(CX, rows[2], CW, H, "Deployment controller", "seconds")
    d.node(CX, rows[3], CW, H, "Catalog pods", None, "store")
    d.node(CX, rows[4], CW, H, "Nodes", None, "store")
    d.node(624, rows[2], 216, H, "kubectl scale", "a person's head", "optional")
    d.node(624, rows[3], 216, H, "Cluster autoscaler", "~1 min plus node boot")
    d.node(24, rows[4], 192, H, "Node-upgrade reconciler", "platform config")
    d.note(624, 72, "Slower loops set the set points", anchor="start")
    d.note(624, 88, "of faster ones: a hierarchy,", anchor="start")
    d.note(624, 104, "not a fight.", anchor="start")
    d.note(624, 168, "One field, one owner: policy", anchor="start")
    d.note(624, 184, "rejects replicas beside an HPA.", anchor="start")
    d.legend([("store", "Desired state or resource"), ("backend", "Controller loop"), ("optional", "Human"),
              ("arrow:muted", "Writes"), ("arrow:link:dashed", "Observes"), ("arrow:accent:dashed", "Second owner")])
    return d
