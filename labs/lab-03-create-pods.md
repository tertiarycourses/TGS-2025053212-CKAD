# Lab 3 — Create and Manage Pods

The Pod is the smallest schedulable unit in Kubernetes. In this lab you will create Pods imperatively, generate YAML with `--dry-run`, edit live manifests, and use the exam-critical `$do` alias that saves 30+ seconds per question.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `nginx:1.25`, `busybox` images (pulled automatically)

---

## Step 1 — Set exam-speed aliases

```bash
alias k=kubectl
export do="--dry-run=client -o yaml"
echo 'alias k=kubectl' >> ~/.bashrc
echo 'export do="--dry-run=client -o yaml"' >> ~/.bashrc
```

These two lines are the first thing to run on CKAD exam day. Every step below uses them.

---

## Step 2 — Create a Pod imperatively

```bash
k run web --image=nginx:1.25 --port=80
k get pod web -o wide
```

`kubectl run` is the fastest path to a running Pod. `-o wide` shows the node and Pod IP.

---

## Step 3 — Generate a Pod manifest without creating it

```bash
k run web2 --image=nginx:1.25 --port=80 $do > web2.yaml
cat web2.yaml
```

`$do` expands to `--dry-run=client -o yaml`. Redirect to a file, edit, then apply — the standard CKAD workflow.

---

## Step 4 — Add a label and apply the manifest

```bash
sed -i 's/^  labels:.*/  labels:\n    tier: frontend/' web2.yaml
k apply -f web2.yaml
k get pod web2 --show-labels
```

`kubectl apply` is idempotent — safe to run multiple times.

---

## Step 5 — Inspect a running Pod

```bash
k describe pod web
k get pod web -o jsonpath='{.status.podIP}'; echo
```

`describe` shows Events, image pulls, volume mounts, and probe status — the primary debugging tool. `jsonpath` extracts single fields for scripting.

---

## Step 6 — Override the container command

```bash
k run sleeper --image=busybox --restart=Never -- sh -c 'sleep 3600'
k get pod sleeper
k logs sleeper || echo "no output — container is sleeping"
```

`--restart=Never` creates a bare Pod (not a Deployment). Everything after `--` becomes the container command and arguments.

---

## Step 7 — Clean up

```bash
k delete pod web web2 sleeper --force --grace-period=0
```

`--force --grace-period=0` skips the 30-second termination grace period — use this in the exam to save time.

---

## Free online tools

- **kubectl cheat sheet** (allowed in exam): https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- **killer.sh** — CKAD mock exam simulator: https://killer.sh
- **JSONPath reference**: https://kubernetes.io/docs/reference/kubectl/jsonpath/
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `alias k=kubectl` and `export do="--dry-run=client -o yaml"` — set these first on exam day.
- `kubectl run` for imperative Pods; `kubectl apply -f` for declarative manifests.
- `--restart=Never` + `--` separator for bare Pods with custom commands.
- `kubectl describe` for events; `jsonpath` for field extraction.
