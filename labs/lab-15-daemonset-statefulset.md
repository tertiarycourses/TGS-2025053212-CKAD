# Lab 15 — DaemonSets and StatefulSets

A **DaemonSet** runs one Pod per (selected) node — used for log collectors, node exporters, CNI agents. A **StatefulSet** gives Pods stable identities and ordered startup — used for databases, queues, leader-elected services. In this lab you will create both and observe the differences from a Deployment.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — DaemonSet on every node

```bash
alias k=kubectl
cat > ds.yaml <<'EOF'
apiVersion: apps/v1
kind: DaemonSet
metadata: { name: node-agent }
spec:
  selector: { matchLabels: { app: node-agent } }
  template:
    metadata: { labels: { app: node-agent } }
    spec:
      tolerations:
      - operator: Exists           # also schedule on control-plane in Killercoda
      containers:
      - name: agent
        image: busybox
        command: ["sh","-c","while true; do echo agent on $(hostname); sleep 30; done"]
EOF
k apply -f ds.yaml
k get ds,pods -l app=node-agent -o wide
```

The `DESIRED` and `CURRENT` counts equal the number of nodes.

---

## Step 2 — Headless Service for the StatefulSet

```bash
cat > headless.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata: { name: db }
spec:
  clusterIP: None
  selector: { app: db }
  ports: [{ port: 5432, name: pg }]
EOF
k apply -f headless.yaml
```

`clusterIP: None` gives every Pod a DNS name like `db-0.db.default.svc.cluster.local`.

---

## Step 3 — StatefulSet with stable identities

```bash
cat > sts.yaml <<'EOF'
apiVersion: apps/v1
kind: StatefulSet
metadata: { name: db }
spec:
  serviceName: db
  replicas: 3
  selector: { matchLabels: { app: db } }
  template:
    metadata: { labels: { app: db } }
    spec:
      containers:
      - name: db
        image: busybox
        command: ["sh","-c","echo $(hostname) ready; sleep 3600"]
EOF
k apply -f sts.yaml
k rollout status sts/db
k get pods -l app=db
```

Pods are created in order: `db-0`, then `db-1`, then `db-2`. Deletion is reverse order.

---

## Step 4 — Verify stable DNS

```bash
k run probe --image=busybox --restart=Never -it --rm -- sh -c '
nslookup db-0.db.default.svc.cluster.local;
nslookup db.default.svc.cluster.local'
```

The first lookup returns one Pod's IP; the second returns all three (headless).

---

## Step 5 — Scale a StatefulSet

```bash
k scale sts db --replicas=4
k get pods -l app=db -w   # watch db-3 appear; ctrl+C
k scale sts db --replicas=2
```

`db-3` is removed before `db-2`. Scale-down is always highest ordinal first.

---

## Step 6 — Clean up

```bash
k delete ds node-agent
k delete sts db
k delete svc db
```

---

## What you learned
- DaemonSet = one Pod per (matching) node.
- StatefulSet = stable network identity + ordered start/stop.
- Headless Service (`clusterIP: None`) for per-Pod DNS.
