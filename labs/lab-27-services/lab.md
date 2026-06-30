# Lab 27 — Services (ClusterIP, NodePort, LoadBalancer)

A Service gives a stable virtual IP and DNS name to a set of Pods. CKAD 2026 requires fluency with `ClusterIP`, `NodePort`, and `LoadBalancer` types, `kubectl expose`, endpoint debugging, and the selector-mismatch pattern.

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

## Step 2 — Create the backend Deployment

```bash
k create deployment web --image=nginx:1.25 --replicas=3
k get pods -l app=web
```

---

## Step 3 — ClusterIP Service (in-cluster only)

```bash
k expose deployment web --port=80 --target-port=80 --name=web-cip
k get svc web-cip
k describe svc web-cip | grep -E "IP:|Endpoints:"
```

Test from inside the cluster:

```bash
k run probe --image=busybox --restart=Never -it --rm -- wget -qO- web-cip
```

A ClusterIP is reachable only by other Pods in the cluster — not from outside.

---

## Step 4 — NodePort Service (exposes a port on every node)

```bash
k expose deployment web --port=80 --target-port=80 \
  --type=NodePort --name=web-np
PORT=$(k get svc web-np -o jsonpath='{.spec.ports[0].nodePort}')
echo "NodePort=$PORT"
curl -s http://localhost:$PORT | head -3
```

NodePort opens the same TCP port (30000–32767 range) on every node in the cluster.

---

## Step 5 — LoadBalancer Service

```bash
k expose deployment web --port=80 --target-port=80 \
  --type=LoadBalancer --name=web-lb
k get svc web-lb
```

On a cloud provider this provisions a public load balancer. On Killercoda, `EXTERNAL-IP` stays `<pending>` (no cloud LB controller). The NodePort it allocates is still usable.

---

## Step 6 — EndpointSlices

```bash
k get endpoints web-cip
k get endpointslices -l kubernetes.io/service-name=web-cip
```

EndpointSlices (v1.21+) are the successor to Endpoints. Both are updated whenever Pods are added or removed.

---

## Step 7 — Debug a selector mismatch

```bash
k patch svc web-cip -p '{"spec":{"selector":{"app":"does-not-exist"}}}'
k get endpoints web-cip
k patch svc web-cip -p '{"spec":{"selector":{"app":"web"}}}'
```

Empty Endpoints = selector does not match any Pod labels. This is the most common Service bug on the exam.

---

## Step 8 — Clean up

```bash
k delete svc web-cip web-np web-lb
k delete deployment web
```

---

## Free online tools

- **Services docs**: https://kubernetes.io/docs/concepts/services-networking/service/
- **kubectl expose reference**: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_expose/
- **EndpointSlices docs**: https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `ClusterIP` — in-cluster only; `NodePort` — every node gets a port; `LoadBalancer` — cloud LB.
- `kubectl expose deployment` is the fastest one-liner to create a Service.
- Empty `Endpoints` almost always means a selector label mismatch — check with `kubectl describe svc`.
- `kubectl get endpointslices` is the modern successor to `kubectl get endpoints`.
