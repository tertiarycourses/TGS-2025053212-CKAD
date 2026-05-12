# Lab 3 — Create and Manage Pods

The Pod is the smallest deployable unit in Kubernetes. In this lab you will create Pods imperatively, generate Pod YAML on the fly, edit a running Pod, and clean up. You will practice the exam-time pattern: `kubectl run … --dry-run=client -o yaml`.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Set up exam aliases

```bash
alias k=kubectl
export do="--dry-run=client -o yaml"
```

---

## Step 2 — Run an imperative Pod

```bash
k run web --image=nginx:1.25 --port=80
k get pod web -o wide
```

`kubectl run` is the fastest way to create a single Pod.

---

## Step 3 — Generate a Pod manifest without applying

```bash
k run web2 --image=nginx:1.25 --port=80 $do > web2.yaml
cat web2.yaml
```

The `$do` expansion saves typing `--dry-run=client -o yaml` every time.

---

## Step 4 — Edit and apply the manifest

Open `web2.yaml` and add a label, then apply:

```bash
sed -i 's/^  labels:.*/  labels:\n    tier: frontend/' web2.yaml
k apply -f web2.yaml
k get pod web2 --show-labels
```

---

## Step 5 — Inspect a running Pod

```bash
k describe pod web
k get pod web -o jsonpath='{.status.podIP}'; echo
```

`describe` shows events, image pulls, mounts, and probe status. `jsonpath` extracts a single field — useful when piping into shell scripts.

---

## Step 6 — Override the container command

```bash
k run sleeper --image=busybox --restart=Never -- sh -c 'sleep 3600'
k logs sleeper || echo "no output, container is sleeping"
```

`--restart=Never` produces a Pod instead of a Deployment. Everything after `--` becomes the container's command + args.

---

## Step 7 — Clean up

```bash
k delete pod web web2 sleeper --force --grace-period 0
```

---

## What you learned
- Imperative `kubectl run` vs. declarative `kubectl apply -f`.
- The `--dry-run=client -o yaml` pattern to scaffold YAML in seconds.
- How `--restart=Never` and `--` change Pod behaviour.
