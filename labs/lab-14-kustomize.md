# Lab 14 — Kustomize Overlays

Kustomize lets you reuse a **base** set of manifests and apply environment-specific **overlays** — without templating. It is built into `kubectl` (`-k`). In this lab you will build a base, a `dev` overlay, and a `prod` overlay.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Project layout

```bash
mkdir -p ~/lab14/{base,overlays/dev,overlays/prod}
cd ~/lab14
```

---

## Step 2 — Base manifests

```bash
cat > base/deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: { name: web }
spec:
  replicas: 1
  selector: { matchLabels: { app: web } }
  template:
    metadata: { labels: { app: web } }
    spec:
      containers:
      - name: web
        image: nginx:1.25
EOF

cat > base/service.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata: { name: web }
spec:
  selector: { app: web }
  ports: [{ port: 80, targetPort: 80 }]
EOF

cat > base/kustomization.yaml <<'EOF'
resources:
- deployment.yaml
- service.yaml
EOF
```

---

## Step 3 — Dev overlay (1 replica, `dev-` name prefix)

```bash
cat > overlays/dev/kustomization.yaml <<'EOF'
resources:
- ../../base
namePrefix: dev-
commonLabels:
  env: dev
EOF
```

---

## Step 4 — Prod overlay (5 replicas + image bump)

```bash
cat > overlays/prod/replica-patch.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: { name: web }
spec:
  replicas: 5
EOF

cat > overlays/prod/kustomization.yaml <<'EOF'
resources:
- ../../base
namePrefix: prod-
commonLabels:
  env: prod
images:
- name: nginx
  newTag: "1.26"
patches:
- path: replica-patch.yaml
EOF
```

---

## Step 5 — Preview each overlay

```bash
kubectl kustomize overlays/dev | head -30
kubectl kustomize overlays/prod | head -30
```

---

## Step 6 — Apply the dev overlay

```bash
kubectl apply -k overlays/dev
kubectl get deploy,svc -l env=dev
```

---

## Step 7 — Switch to prod

```bash
kubectl apply -k overlays/prod
kubectl get deploy,svc -l env=prod
kubectl describe deploy prod-web | grep Image:
```

---

## Step 8 — Clean up

```bash
kubectl delete -k overlays/dev
kubectl delete -k overlays/prod
```

---

## What you learned
- Base + overlays = reuse without templating.
- `namePrefix`, `commonLabels`, `images`, and strategic-merge `patches`.
- `kubectl apply -k` and `kubectl kustomize` are built into kubectl.
