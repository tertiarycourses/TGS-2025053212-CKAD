# Lab 11 — Blue/Green Deployment

Blue/Green keeps two complete copies of an application alive. A Service selector switch flips all traffic from blue (current) to green (next) in one atomic step. In this lab you will build both colours and flip the Service.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Blue Deployment + Service

```bash
alias k=kubectl
cat > blue.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: { name: web-blue }
spec:
  replicas: 3
  selector: { matchLabels: { app: web, version: blue } }
  template:
    metadata: { labels: { app: web, version: blue } }
    spec:
      containers:
      - name: web
        image: nginx:1.24
---
apiVersion: v1
kind: Service
metadata: { name: web }
spec:
  selector: { app: web, version: blue }
  ports: [{ port: 80, targetPort: 80 }]
EOF
k apply -f blue.yaml
```

---

## Step 2 — Green Deployment (not yet receiving traffic)

```bash
cat > green.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: { name: web-green }
spec:
  replicas: 3
  selector: { matchLabels: { app: web, version: green } }
  template:
    metadata: { labels: { app: web, version: green } }
    spec:
      containers:
      - name: web
        image: nginx:1.25
EOF
k apply -f green.yaml
k get pods -l app=web --show-labels
```

Both colours are running. The Service still selects only `version: blue`.

---

## Step 3 — Smoke-test green directly

```bash
GREEN_POD=$(k get pod -l version=green -o jsonpath='{.items[0].metadata.name}')
k exec $GREEN_POD -- curl -sI localhost:80 | head -1
```

---

## Step 4 — Flip the Service to green

```bash
k patch service web -p '{"spec":{"selector":{"app":"web","version":"green"}}}'
k describe svc web | grep Selector
```

Traffic now points at green Pods only. Blue is still running as a fallback.

---

## Step 5 — Roll back instantly

```bash
k patch service web -p '{"spec":{"selector":{"app":"web","version":"blue"}}}'
```

The whole rollback is a single Service patch — milliseconds, no Pod churn.

---

## Step 6 — Decommission blue

When confident, delete the old Deployment:

```bash
k delete deployment web-blue
```

---

## Step 7 — Clean up

```bash
k delete deployment web-green --ignore-not-found
k delete service web
```

---

## What you learned
- Blue/Green = two Deployments, one Service.
- Atomic cutover and rollback via `kubectl patch service … selector`.
- Always validate the new colour out-of-band before flipping.
