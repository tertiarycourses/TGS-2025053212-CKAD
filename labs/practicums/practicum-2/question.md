# Practicum 2 — Application Deployment (Domain 2)

> **Day 2 assessment · Time allowed: 45 minutes**  
> Platform: [Killercoda Kubernetes Playground](https://killercoda.com/playgrounds/scenario/kubernetes)

---

## Task 1 — Create and scale a Deployment (10 pts)

1. Create a Deployment named `api` in namespace `staging` (create the namespace first).
   - Image: `nginx:1.25`
   - Initial replicas: `2`
   - Label: `app=api`
2. Scale it to `4` replicas using `kubectl scale`.
3. Confirm all 4 Pods are `Running`.

---

## Task 2 — Rolling update and rollback (10 pts)

1. Update the `api` Deployment to use image `nginx:1.27`.
2. Watch the rollout with `kubectl rollout status`.
3. Confirm the new image is running.
4. Roll back to the previous version with `kubectl rollout undo`.
5. Confirm the image reverts to `nginx:1.25`.

---

## Task 3 — Blue/Green switch (10 pts)

You have two Deployments already in namespace `default`:

- `blue` (image `nginx:1.25`, label `version=blue`)
- `green` (image `nginx:1.27`, label `version=green`)

A Service `frontend` currently selects `version=blue`.

Switch traffic to the `green` Deployment by patching the Service selector **without deleting either Deployment**.

Verify by describing the Endpoints object for `frontend`.

---

## Task 4 — Helm install and upgrade (10 pts)

1. Add the Bitnami Helm repository:
   ```bash
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo update
   ```
2. Install `nginx` from the Bitnami chart into namespace `helm-test` (create if needed):
   ```bash
   helm install my-nginx bitnami/nginx --namespace helm-test --create-namespace
   ```
3. Upgrade the release, setting `replicaCount=2`.
4. Verify with `helm list -n helm-test` and `kubectl get pods -n helm-test`.

---

## Marking Guide

| Task | Criteria | Points |
|------|----------|--------|
| 1 | Deployment created, scaled to 4, all pods running | 10 |
| 2 | Image updated, rollout clean, rollback successful | 10 |
| 3 | Service selector patched, endpoints point to green pods | 10 |
| 4 | Helm install and upgrade successful, 2 replicas running | 10 |
| **Total** | | **40** |
