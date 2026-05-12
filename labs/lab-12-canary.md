# Lab 12 — Canary Deployment

A canary release sends a fraction of live traffic to a new version while keeping the bulk on the stable version. In this lab you will achieve weighted traffic by adjusting replica ratios behind a single Service.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Stable Deployment (9 replicas)

```bash
alias k=kubectl
cat > stable.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: { name: web-stable }
spec:
  replicas: 9
  selector: { matchLabels: { app: web, track: stable } }
  template:
    metadata: { labels: { app: web, track: stable } }
    spec:
      containers:
      - name: web
        image: hashicorp/http-echo
        args: ["-text=stable"]
---
apiVersion: v1
kind: Service
metadata: { name: web }
spec:
  selector: { app: web }
  ports: [{ port: 5678, targetPort: 5678 }]
EOF
k apply -f stable.yaml
```

The Service selector uses **only** `app: web` so it covers both stable and canary Pods.

---

## Step 2 — Canary Deployment (1 replica = ~10%)

```bash
cat > canary.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: { name: web-canary }
spec:
  replicas: 1
  selector: { matchLabels: { app: web, track: canary } }
  template:
    metadata: { labels: { app: web, track: canary } }
    spec:
      containers:
      - name: web
        image: hashicorp/http-echo
        args: ["-text=canary"]
EOF
k apply -f canary.yaml
```

10 total Pods (9 stable + 1 canary) → roughly 10 % of requests hit the canary.

---

## Step 3 — Verify the split

```bash
k run probe --image=busybox --restart=Never -it --rm -- sh -c '
for i in $(seq 1 30); do wget -qO- web:5678; done | sort | uniq -c'
```

You should see roughly 27 `stable` and 3 `canary` (90/10).

---

## Step 4 — Promote: ramp the canary, retire the stable

```bash
k scale deployment web-canary --replicas=9
k scale deployment web-stable --replicas=0
```

The canary is now the primary. When you are happy, delete the stable Deployment.

---

## Step 5 — Clean up

```bash
k delete deployment web-stable web-canary
k delete service web
```

---

## What you learned
- Canary = two Deployments behind one broad Service selector.
- Traffic split is approximated by replica count ratio.
- Promotion is just `kubectl scale` on both Deployments.
