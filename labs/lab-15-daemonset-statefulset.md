# Lab 15 — DaemonSets and StatefulSets

A DaemonSet runs exactly one Pod per matching node — used for log collectors, CNI agents, and node exporters. A StatefulSet gives Pods stable network identities and ordered start/stop — used for databases and leader-elected services. CKAD 2026 expects you to know when to use each and how to write the YAML.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `busybox` image (pre-pulled on Killercoda)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
```

---

## Step 2 — DaemonSet on every node

```bash
cat > ds.yaml <<'EOF'
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-agent
spec:
  selector:
    matchLabels:
      app: node-agent
  template:
    metadata:
      labels:
        app: node-agent
    spec:
      tolerations:
      - operator: Exists
      containers:
      - name: agent
        image: busybox
        command: ["sh", "-c", "while true; do echo agent on $(hostname); sleep 30; done"]
EOF
k apply -f ds.yaml
k get ds,pods -l app=node-agent -o wide
```

`tolerations: - operator: Exists` schedules the DaemonSet Pod on control-plane nodes too — required in Killercoda's single-node setup. The `DESIRED` count matches the node count.

---

## Step 3 — Headless Service for the StatefulSet

```bash
cat > headless.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: db
spec:
  clusterIP: None
  selector:
    app: db
  ports:
  - port: 5432
    name: pg
EOF
k apply -f headless.yaml
```

`clusterIP: None` makes this headless — DNS returns individual Pod IPs, not a virtual IP.

---

## Step 4 — StatefulSet with stable identities

```bash
cat > sts.yaml <<'EOF'
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
spec:
  serviceName: db
  replicas: 3
  selector:
    matchLabels:
      app: db
  template:
    metadata:
      labels:
        app: db
    spec:
      containers:
      - name: db
        image: busybox
        command: ["sh", "-c", "echo $(hostname) ready; sleep 3600"]
EOF
k apply -f sts.yaml
k rollout status sts/db
k get pods -l app=db
```

Pods are created in strict order: `db-0` → `db-1` → `db-2`. Deletion reverses the order: `db-2` → `db-1` → `db-0`.

---

## Step 5 — Verify stable per-Pod DNS

```bash
k run probe --image=busybox --restart=Never -it --rm -- sh -c \
  'nslookup db-0.db.default.svc.cluster.local; nslookup db.default.svc.cluster.local'
```

`db-0.db.default.svc.cluster.local` resolves to one Pod's IP. The headless Service DNS returns all three.

---

## Step 6 — Scale a StatefulSet

```bash
k scale sts db --replicas=4
k get pods -l app=db -w
k scale sts db --replicas=2
```

Scale-down always terminates the highest ordinal first (`db-3`, then `db-2` if going to 2).

---

## Step 7 — Clean up

```bash
k delete ds node-agent
k delete sts db
k delete svc db
```

---

## Free online tools

- **DaemonSet docs**: https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/
- **StatefulSet docs**: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- DaemonSet = one Pod per matching node; `tolerations` control which nodes are included.
- StatefulSet = stable Pod names (`<name>-0`, `<name>-1`) and ordered start/stop.
- Headless Service (`clusterIP: None`) is required for per-Pod DNS in a StatefulSet.
- Scale-down order is always highest ordinal first.
