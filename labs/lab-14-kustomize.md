# Lab 14 — Kustomize Overlays

Kustomize lets you reuse a single **base** set of manifests and apply environment-specific **overlays** without templating. It is built into `kubectl` (`-k` flag) — no installation required. CKAD 2026 tests `namePrefix`, `commonLabels`, `images`, and strategic-merge `patches`.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda — includes kustomize)
- `nginx:1.25`, `nginx:1.26` images (pulled automatically)

---

## Step 1 — Create the project layout

```bash
mkdir -p ~/lab14/{base,overlays/dev,overlays/prod}
cd ~/lab14
```

---

## Step 2 — Base manifests (shared by all environments)

```bash
cat > base/deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 1
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: nginx:1.25
EOF

cat > base/service.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
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

## Step 4 — Prod overlay (5 replicas, image bump to 1.26)

```bash
cat > overlays/prod/replica-patch.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
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

## Step 5 — Preview without applying

```bash
kubectl kustomize overlays/dev | grep -E "name:|replicas:|image:"
kubectl kustomize overlays/prod | grep -E "name:|replicas:|image:"
```

Dev: name `dev-web`, 1 replica, `nginx:1.25`. Prod: name `prod-web`, 5 replicas, `nginx:1.26`.

---

## Step 6 — Apply the dev overlay

```bash
kubectl apply -k overlays/dev
kubectl get deploy,svc -l env=dev
```

---

## Step 7 — Apply the prod overlay and verify image

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

## Free online tools

- **Kustomize docs**: https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
- **Kustomize reference site**: https://kustomize.io
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Base + overlays = reuse without Go templating.
- `namePrefix` and `commonLabels` are applied to every resource in the overlay.
- `images` block overrides image tags without editing base files.
- `kubectl apply -k` and `kubectl kustomize` are built into kubectl — no extra binary.
