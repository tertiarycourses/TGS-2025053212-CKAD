# Lab 10 — Rolling Updates and Rollback

A Deployment performs zero-downtime upgrades by rolling Pods one ReplicaSet at a time. In this lab you will update an image, watch the rollout, pause and resume it, and roll back to the previous revision.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Create the initial Deployment

```bash
alias k=kubectl
k create deployment web --image=nginx:1.24 --replicas=4
k rollout status deployment/web
```

---

## Step 2 — Tune the rolling-update strategy

```bash
k patch deployment web -p '{"spec":{"strategy":{"rollingUpdate":{"maxSurge":1,"maxUnavailable":1}}}}'
k describe deployment web | grep -A3 RollingUpdateStrategy
```

- `maxSurge` — extra Pods allowed above desired during the rollout.
- `maxUnavailable` — Pods allowed to be down during the rollout.

---

## Step 3 — Trigger an image update

```bash
k set image deployment/web nginx=nginx:1.25
k rollout status deployment/web
k get rs -l app=web
```

You will see the old ReplicaSet drain to 0 while the new ReplicaSet ramps to 4.

---

## Step 4 — View rollout history

```bash
k rollout history deployment/web
k rollout history deployment/web --revision=2
```

---

## Step 5 — Pause and resume

```bash
k rollout pause deployment/web
k set image deployment/web nginx=nginx:1.26
k set env deployment/web COLOR=green
k rollout resume deployment/web   # both changes ship together
k rollout status deployment/web
```

Pausing batches multiple changes into a single new ReplicaSet.

---

## Step 6 — Roll back

```bash
k rollout undo deployment/web
k rollout status deployment/web
k describe deployment web | grep Image:
```

To roll back to a specific revision: `k rollout undo deployment/web --to-revision=2`.

---

## Step 7 — Clean up

```bash
k delete deployment web
```

---

## What you learned
- `kubectl set image`, `kubectl rollout status`, `kubectl rollout undo`.
- `maxSurge` / `maxUnavailable` control rollout aggressiveness.
- `kubectl rollout pause` lets you batch multiple changes into one ReplicaSet.
