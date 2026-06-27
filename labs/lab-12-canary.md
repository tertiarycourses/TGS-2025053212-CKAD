# Lab 12 — Canary Deployment

A canary release sends a small fraction of live traffic to a new version while keeping the bulk on the stable version. In Kubernetes, traffic split is approximated by controlling replica ratios behind a single broad Service selector — no special tooling required.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `hashicorp/http-echo` image (pulled automatically)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
```

---

## Step 2 — Stable Deployment (90% of traffic)

```bash
cat > stable.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: web
      track: stable
  template:
    metadata:
      labels:
        app: web
        track: stable
    spec:
      containers:
      - name: web
        image: hashicorp/http-echo
        args: ["-text=stable"]
---
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
  ports:
  - port: 5678
    targetPort: 5678
EOF
k apply -f stable.yaml
```

The Service selector uses only `app: web` — it routes to **both** stable and canary Pods. Traffic split is determined by replica count ratio.

---

## Step 3 — Canary Deployment (10% of traffic)

```bash
cat > canary.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: web
      track: canary
  template:
    metadata:
      labels:
        app: web
        track: canary
    spec:
      containers:
      - name: web
        image: hashicorp/http-echo
        args: ["-text=canary"]
EOF
k apply -f canary.yaml
k get pods -l app=web --show-labels
```

9 stable + 1 canary = roughly 10% of requests hit the canary.

---

## Step 4 — Verify the traffic split

```bash
k run probe --image=busybox --restart=Never -it --rm -- sh -c \
  'for i in $(seq 1 30); do wget -qO- web:5678; done | sort | uniq -c'
```

Expected: approximately 27 `stable` and 3 `canary` lines.

---

## Step 5 — Promote: scale up canary, retire stable

```bash
k scale deployment web-canary --replicas=9
k scale deployment web-stable --replicas=0
```

Once the canary is fully promoted, delete the stable Deployment.

---

## Step 6 — Clean up

```bash
k delete deployment web-stable web-canary --ignore-not-found
k delete service web
```

---

## Free online tools

- **Canary deployments on Kubernetes**: https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/#canary-deployments
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Canary = two Deployments with different `track` labels behind one broad Service selector.
- Traffic split is approximated by replica ratio (9:1 ≈ 90%/10%).
- Promotion is `kubectl scale` on both Deployments — no Service change needed.
- For precise percentage splits, use a service mesh (Istio/Linkerd) — beyond CKAD scope.
