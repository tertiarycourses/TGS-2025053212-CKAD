# Lab 28 — Service DNS

CoreDNS gives every Service a stable DNS name. The canonical FQDN is `<svc>.<ns>.svc.cluster.local`. In this lab you will resolve Services from different namespaces and confirm Pod-to-Pod DNS.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Create services in two namespaces

```bash
alias k=kubectl
k create ns app
k create ns probe

k -n app create deployment web --image=nginx:1.25 --replicas=2
k -n app expose deployment web --port=80
```

---

## Step 2 — Resolve the Service from the same namespace

```bash
k -n app run client --image=busybox --restart=Never -it --rm -- sh -c '
nslookup web
wget -qO- web | head -3'
```

`web` alone resolves because the client Pod is in the same namespace.

---

## Step 3 — Resolve from a different namespace

```bash
k -n probe run client --image=busybox --restart=Never -it --rm -- sh -c '
nslookup web 2>&1 || true
nslookup web.app
nslookup web.app.svc.cluster.local'
```

Cross-namespace lookups need at least `<svc>.<ns>`.

---

## Step 4 — Pod DNS records

```bash
POD_IP=$(k -n app get pod -l app=web -o jsonpath='{.items[0].status.podIP}')
DASHED=$(echo $POD_IP | tr . -)
k -n probe run client --image=busybox --restart=Never -it --rm -- nslookup $DASHED.app.pod.cluster.local
```

Every Pod gets a DNS name of the form `<dashed-ip>.<ns>.pod.cluster.local`.

---

## Step 5 — Inspect the resolver config

```bash
k -n app run shell --image=busybox --restart=Never -it --rm -- cat /etc/resolv.conf
```

You will see:

```
nameserver 10.96.0.10
search app.svc.cluster.local svc.cluster.local cluster.local
ndots:5
```

`ndots:5` is why a single-label name like `web` triggers up to five DNS lookups.

---

## Step 6 — Headless Service vs ClusterIP

```bash
k -n app create service clusterip headless --clusterip="None" --tcp=80:80
k -n app patch service headless -p '{"spec":{"selector":{"app":"web"}}}'
k -n probe run h --image=busybox --restart=Never -it --rm -- nslookup headless.app
```

A headless Service returns **all** Pod IPs instead of one virtual ClusterIP.

---

## Step 7 — Clean up

```bash
k delete ns app probe
```

---

## What you learned
- DNS naming: `<svc>`, `<svc>.<ns>`, `<svc>.<ns>.svc.cluster.local`.
- Pod DNS: `<dashed-ip>.<ns>.pod.cluster.local`.
- `ndots:5` and the `search` list in `/etc/resolv.conf`.
