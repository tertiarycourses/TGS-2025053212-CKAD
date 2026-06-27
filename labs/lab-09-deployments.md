# Lab 9 — Deployments and ReplicaSets

A Deployment manages a ReplicaSet, which manages Pods. CKAD 2026 tests the full ownership chain, scaling, environment variable injection, and reading ReplicaSet history. Understanding this chain is required to debug failed rollouts.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `nginx:1.25`, `httpd:2.4` images (pulled automatically)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
export do="--dry-run=client -o yaml"
```

---

## Step 2 — Create a Deployment imperatively

```bash
k create deployment web --image=nginx:1.25 --replicas=3
k get deploy,rs,pod -l app=web
```

One command creates three resources: Deployment → ReplicaSet (hash-suffixed name) → 3 Pods. The chain is visible in the `-l app=web` output.

---

## Step 3 — Scale up and down

```bash
k scale deployment web --replicas=5
k get pods -l app=web
k scale deployment web --replicas=2
k get pods -l app=web
```

The ReplicaSet controller reconciles the actual count to match desired at all times.

---

## Step 4 — Generate Deployment YAML and apply

```bash
k create deployment api --image=httpd:2.4 --replicas=2 $do > api.yaml
cat api.yaml
k apply -f api.yaml
```

Generate → inspect → apply is the safe CKAD workflow for any new resource.

---

## Step 5 — Inject an environment variable

```bash
k set env deployment/api APP_COLOR=blue
k describe deploy api | grep -A3 Environment
```

`kubectl set env` updates the Pod template, triggering a new ReplicaSet and a rolling update.

---

## Step 6 — Observe ReplicaSet history

```bash
k get rs -l app=api
```

You should see two ReplicaSets: the old one at `0/0/0` and the new one at `2/2/2`. Deployments keep old ReplicaSets for rollback — the count kept is controlled by `revisionHistoryLimit` (default 10).

---

## Step 7 — Clean up

```bash
k delete deployment web api
```

---

## Free online tools

- **Deployments docs**: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- **kubectl set reference**: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_set/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Deployment → ReplicaSet → Pod: the three-tier ownership chain.
- `kubectl scale` changes the replica count; the ReplicaSet controller acts immediately.
- `kubectl set env` / `kubectl set image` mutate the Pod template and trigger a rolling update.
- Old ReplicaSets are kept for rollback — `revisionHistoryLimit` controls how many.
