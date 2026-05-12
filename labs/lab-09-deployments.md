# Lab 9 — Deployments and ReplicaSets

A Deployment manages a ReplicaSet, which in turn manages Pods. In this lab you will create a Deployment, scale it, and inspect the ReplicaSet that Kubernetes automatically creates for you.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Create a Deployment imperatively

```bash
alias k=kubectl
k create deployment web --image=nginx:1.25 --replicas=3
k get deploy,rs,pod -l app=web
```

The output shows three resources created by one command: a Deployment, a ReplicaSet (auto-named with a hash suffix), and three Pods.

---

## Step 2 — Scale up and down

```bash
k scale deployment web --replicas=5
k get pods -l app=web
k scale deployment web --replicas=2
```

ReplicaSet enforces the desired count by creating or deleting Pods.

---

## Step 3 — Generate Deployment YAML

```bash
export do="--dry-run=client -o yaml"
k create deployment api --image=httpd:2.4 --replicas=2 $do > api.yaml
cat api.yaml
k apply -f api.yaml
```

---

## Step 4 — Update an environment variable through the Deployment

```bash
k set env deployment/api COLOR=blue
k describe deploy api | grep -A2 Environment
```

`kubectl set env` mutates the Pod template, which triggers a new ReplicaSet.

---

## Step 5 — Observe ReplicaSet history

```bash
k get rs -l app=api
```

You should see the old ReplicaSet at `0/0/0` and the new one at `2/2/2`. The Deployment keeps both for rollback.

---

## Step 6 — Clean up

```bash
k delete deployment web api
```

---

## What you learned
- Deployment → ReplicaSet → Pod ownership chain.
- `kubectl scale` for replica count.
- `kubectl set env` and `kubectl set image` mutate the Pod template safely.
