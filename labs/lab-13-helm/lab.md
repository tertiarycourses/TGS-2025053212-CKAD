# Lab 13 — Helm: Install, Upgrade, and Rollback

Helm is the Kubernetes package manager. A chart is a bundle of YAML templates; a release is a deployed instance. CKAD 2026 tests `helm install`, `helm upgrade`, `helm rollback`, `helm list`, and value overrides — all under exam time pressure.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `helm` (install in Step 1 — one command)
- `kubectl` (pre-installed on Killercoda)
- Bitnami nginx chart (downloaded from chart repo)

---

## Step 1 — Install Helm

```bash
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```

---

## Step 2 — Add the Bitnami chart repository

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo bitnami/nginx | head -5
```

---

## Step 3 — Install a release with value overrides

```bash
helm install web bitnami/nginx \
  --set service.type=ClusterIP \
  --set replicaCount=2
helm list
kubectl get pods -l app.kubernetes.io/instance=web
```

The release name `web` is what you reference for all subsequent commands. `--set key=value` overrides chart defaults.

---

## Step 4 — Inspect the generated manifests and values

```bash
helm get manifest web | head -40
helm get values web
```

`helm get manifest` shows the actual YAML Kubernetes received. `helm get values` shows what was overridden.

---

## Step 5 — Upgrade the release

```bash
helm upgrade web bitnami/nginx --set replicaCount=4 --reuse-values
helm history web
kubectl get pods -l app.kubernetes.io/instance=web
```

`--reuse-values` preserves the prior `service.type=ClusterIP` setting while only changing `replicaCount`.

---

## Step 6 — Roll back to revision 1

```bash
helm rollback web 1
helm history web
kubectl get pods -l app.kubernetes.io/instance=web
```

`helm history` lists every revision with its status. Rollback creates a new revision — it does not delete history.

---

## Step 7 — Uninstall the release

```bash
helm uninstall web
helm list
```

---

## Free online tools

- **Helm docs**: https://helm.sh/docs/
- **Artifact Hub** — search public charts: https://artifacthub.io
- **Bitnami charts**: https://github.com/bitnami/charts
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Core Helm workflow: `repo add` → `install` → `upgrade` → `rollback` → `uninstall`.
- `--set` overrides chart values at install/upgrade time; `--reuse-values` preserves prior overrides.
- `helm history <release>` tracks every revision for audit and rollback.
- `helm get manifest` is the escape hatch to see what Helm actually sent to Kubernetes.
