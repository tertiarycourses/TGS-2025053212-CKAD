# Lab 28 — Service DNS

CoreDNS gives every Service a stable DNS name. The full FQDN is `<service>.<namespace>.svc.cluster.local`. CKAD 2026 tests cross-namespace DNS resolution, Pod DNS records, headless Services, and reading `/etc/resolv.conf` to understand `ndots:5`.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `nginx:1.25`, `busybox` images (pulled automatically)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
```

---

## Step 2 — Create Services in two namespaces

```bash
k create ns app
k create ns probe

k -n app create deployment web --image=nginx:1.25 --replicas=2
k -n app expose deployment web --port=80
```

---

## Step 3 — Resolve from the same namespace (short name)

```bash
k -n app run client --image=busybox --restart=Never -it --rm -- sh -c \
  'nslookup web; wget -qO- web | head -3'
```

Within the same namespace, `web` resolves because the Pod's search domain includes `app.svc.cluster.local`.

---

## Step 4 — Resolve from a different namespace (needs namespace suffix)

```bash
k -n probe run client --image=busybox --restart=Never -it --rm -- sh -c \
  'nslookup web 2>&1 | head -2;
   nslookup web.app 2>&1 | head -2;
   nslookup web.app.svc.cluster.local | head -3'
```

Cross-namespace lookups require at least `<service>.<namespace>`. The FQDN always works.

---

## Step 5 — Pod DNS record

```bash
POD_IP=$(k -n app get pod -l app=web -o jsonpath='{.items[0].status.podIP}')
DASHED=$(echo $POD_IP | tr . -)
k -n probe run client --image=busybox --restart=Never -it --rm -- \
  nslookup $DASHED.app.pod.cluster.local
```

Every Pod gets a DNS A record: `<dashed-ip>.<namespace>.pod.cluster.local`.

---

## Step 6 — Inspect /etc/resolv.conf inside a Pod

```bash
k -n app run shell --image=busybox --restart=Never -it --rm -- cat /etc/resolv.conf
```

Expected output:
```
nameserver 10.96.0.10
search app.svc.cluster.local svc.cluster.local cluster.local
ndots:5
```

`ndots:5` means any name with fewer than 5 dots triggers the search list first, then an absolute lookup. This is why `web` works within the namespace but `web.app` is needed cross-namespace.

---

## Step 7 — Headless Service returns all Pod IPs

```bash
k -n app create service clusterip headless --clusterip="None" --tcp=80:80
k -n app patch service headless -p '{"spec":{"selector":{"app":"web"}}}'
k -n probe run h --image=busybox --restart=Never -it --rm -- nslookup headless.app
```

A headless Service (`clusterIP: None`) returns all Pod IPs in DNS instead of a single virtual IP.

---

## Step 8 — Clean up

```bash
k delete ns app probe
```

---

## Free online tools

- **DNS for Services and Pods**: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/
- **CoreDNS docs**: https://coredns.io/docs/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- FQDN format: `<service>.<namespace>.svc.cluster.local`.
- Within the same namespace, the short name `<service>` resolves via the search list.
- Cross-namespace: use at minimum `<service>.<namespace>`.
- `ndots:5` explains why short names check the search list before doing absolute DNS.
- Headless Service (`clusterIP: None`) returns per-Pod IPs instead of a virtual IP.
