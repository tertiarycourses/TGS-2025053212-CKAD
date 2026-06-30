# Lab 11 — Blue/Green Deployment

Blue/Green keeps two complete copies of the application alive simultaneously. A Service selector switch flips 100% of traffic from the old version (blue) to the new version (green) in one atomic operation — with instant rollback if anything breaks.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `nginx:1.24`, `nginx:1.25` images (pulled automatically)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
```

---

## Step 2 — Deploy blue (current production)

```bash
cat > blue.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
      version: blue
  template:
    metadata:
      labels:
        app: web
        version: blue
    spec:
      containers:
      - name: web
        image: nginx:1.24
---
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
    version: blue
  ports:
  - port: 80
    targetPort: 80
EOF
k apply -f blue.yaml
k get pods -l app=web --show-labels
```

---

## Step 3 — Deploy green (next version, no live traffic yet)

```bash
cat > green.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
      version: green
  template:
    metadata:
      labels:
        app: web
        version: green
    spec:
      containers:
      - name: web
        image: nginx:1.25
EOF
k apply -f green.yaml
k get pods -l app=web --show-labels
```

Both colours are running. The Service selector still sends all traffic to `version: blue`.

---

## Step 4 — Smoke-test green directly before cutover

```bash
GREEN_POD=$(k get pod -l version=green -o jsonpath='{.items[0].metadata.name}')
k exec $GREEN_POD -- curl -sI localhost:80 | head -2
```

Validate green is healthy before switching traffic.

---

## Step 5 — Flip the Service to green (atomic cutover)

```bash
k patch service web -p '{"spec":{"selector":{"app":"web","version":"green"}}}'
k describe svc web | grep Selector
```

All traffic now routes to green Pods. Blue Pods are still running as an instant fallback.

---

## Step 6 — Roll back instantly (if needed)

```bash
k patch service web -p '{"spec":{"selector":{"app":"web","version":"blue"}}}'
```

Rollback is a single selector patch — milliseconds, no Pod churn.

---

## Step 7 — Decommission blue after confidence

```bash
k delete deployment web-blue
k delete deployment web-green
k delete service web
```

---

## Free online tools

- **Deployment strategies overview**: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Blue/Green = two Deployments with distinct `version` labels, one Service.
- Cutover is a `kubectl patch service` selector update — atomic and instant.
- Rollback is equally instant: patch the selector back to `version: blue`.
- Validate the new colour out-of-band (exec/curl) before flipping live traffic.
