# Lab 13 — Helm Install and Upgrade

Helm is the package manager for Kubernetes. In this lab you will install Helm, deploy a public chart, override values, then upgrade and roll back a release.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Install Helm

```bash
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```

---

## Step 2 — Add the Bitnami chart repo

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo bitnami/nginx | head
```

---

## Step 3 — Install a release with overrides

```bash
helm install web bitnami/nginx \
  --set service.type=ClusterIP \
  --set replicaCount=2
helm list
kubectl get pods -l app.kubernetes.io/instance=web
```

The release name `web` is what you reference for upgrade or rollback.

---

## Step 4 — Inspect generated manifests

```bash
helm get manifest web | head -40
helm get values web
```

---

## Step 5 — Upgrade the release

```bash
helm upgrade web bitnami/nginx --set replicaCount=4 --reuse-values
helm history web
kubectl get pods -l app.kubernetes.io/instance=web
```

`--reuse-values` keeps the prior `--set` values so you only change what you want.

---

## Step 6 — Roll back

```bash
helm rollback web 1
helm history web
kubectl get pods -l app.kubernetes.io/instance=web
```

---

## Step 7 — Uninstall

```bash
helm uninstall web
helm list
```

---

## What you learned
- `helm repo add`, `helm install`, `helm upgrade`, `helm rollback`, `helm uninstall`.
- Overriding chart values with `--set` and `--values`.
- Helm tracks revisions, so rollback is a single command.
