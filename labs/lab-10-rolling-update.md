# Lab 10 — Rolling Updates and Rollback

A Deployment performs zero-downtime upgrades by gradually replacing Pods one ReplicaSet at a time. CKAD 2026 tests `maxSurge`, `maxUnavailable`, rollout pause/resume, history inspection, and rollback — frequently as a multi-step question under time pressure.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `nginx:1.24`, `nginx:1.25`, `nginx:1.26` images (pulled automatically)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
```

---

## Step 2 — Create the initial Deployment

```bash
k create deployment web --image=nginx:1.24 --replicas=4
k rollout status deployment/web
```

---

## Step 3 — Tune the rolling-update strategy

```bash
k patch deployment web -p \
  '{"spec":{"strategy":{"rollingUpdate":{"maxSurge":1,"maxUnavailable":1}}}}'
k describe deployment web | grep -A4 RollingUpdateStrategy
```

- `maxSurge: 1` — at most 1 extra Pod above desired during the rollout
- `maxUnavailable: 1` — at most 1 Pod may be unavailable during the rollout

---

## Step 4 — Trigger an image update and watch the rollout

```bash
k set image deployment/web nginx=nginx:1.25
k rollout status deployment/web
k get rs -l app=web
```

Watch the old ReplicaSet drain to 0 while the new one ramps to 4.

---

## Step 5 — View rollout history

```bash
k rollout history deployment/web
k rollout history deployment/web --revision=2
```

Each `kubectl set image` or Pod-template mutation creates a new revision entry.

---

## Step 6 — Pause, apply multiple changes, then resume

```bash
k rollout pause deployment/web
k set image deployment/web nginx=nginx:1.26
k set env deployment/web APP_ENV=production
k rollout resume deployment/web
k rollout status deployment/web
```

Pausing batches multiple mutations into a single new ReplicaSet — one rollout, not two.

---

## Step 7 — Roll back to the previous revision

```bash
k rollout undo deployment/web
k rollout status deployment/web
k describe deployment web | grep Image:
```

To target a specific revision: `k rollout undo deployment/web --to-revision=1`

---

## Step 8 — Clean up

```bash
k delete deployment web
```

---

## Free online tools

- **Rolling update docs**: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment
- **kubectl rollout reference**: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `kubectl set image` triggers a rolling update; `kubectl rollout status` watches it.
- `maxSurge` and `maxUnavailable` tune rollout speed vs. availability trade-off.
- `kubectl rollout pause` batches multiple changes into one ReplicaSet revision.
- `kubectl rollout undo` reverts to the previous (or specified) revision instantly.
