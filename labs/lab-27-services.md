# Lab 27 — Services (ClusterIP, NodePort, LoadBalancer)

A Service gives a stable IP and DNS name to a set of Pods. CKAD requires fluency with the three core Service types: `ClusterIP` (in-cluster), `NodePort` (exposes a port on every node), and `LoadBalancer` (cloud LB). In this lab you will create all three.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Backend Deployment

```bash
alias k=kubectl
k create deployment web --image=nginx:1.25 --replicas=3
k label deployment web tier=frontend --overwrite
```

---

## Step 2 — ClusterIP Service

```bash
k expose deployment web --port=80 --target-port=80 --name=web-cip
k get svc web-cip
k describe svc web-cip | grep -E 'IP:|Endpoints:'
```

A ClusterIP is reachable only inside the cluster.

```bash
k run probe --image=busybox --restart=Never -it --rm -- wget -qO- web-cip
```

---

## Step 3 — NodePort Service

```bash
k expose deployment web --port=80 --target-port=80 \
  --type=NodePort --name=web-np
PORT=$(k get svc web-np -o jsonpath='{.spec.ports[0].nodePort}')
echo "NodePort=$PORT"
curl -s http://localhost:$PORT | head -3
```

NodePort opens the same TCP port on every node in the range 30000–32767.

---

## Step 4 — LoadBalancer Service

```bash
k expose deployment web --port=80 --target-port=80 \
  --type=LoadBalancer --name=web-lb
k get svc web-lb
```

On a cloud provider this gets a public IP from the cloud LB controller. On Killercoda there is no cloud LB, so `EXTERNAL-IP` stays `<pending>` — but you can still reach it via the NodePort that the LB type also allocates.

---

## Step 5 — Endpoints and EndpointSlices

```bash
k get endpoints web-cip
k get endpointslices -l kubernetes.io/service-name=web-cip
```

EndpointSlices are the v1.21+ successor to Endpoints — both still exist for compatibility.

---

## Step 6 — Selector mismatch debugging

```bash
k patch svc web-cip -p '{"spec":{"selector":{"app":"does-not-exist"}}}'
k get endpoints web-cip      # endpoints empty
k patch svc web-cip -p '{"spec":{"selector":{"app":"web"}}}'
```

Empty Endpoints almost always means the Service selector does not match any Pod labels.

---

## Step 7 — Clean up

```bash
k delete svc web-cip web-np web-lb
k delete deployment web
```

---

## What you learned
- ClusterIP, NodePort, LoadBalancer differences.
- `kubectl expose` as a one-liner Service creator.
- Endpoint membership is selector-driven; mismatched labels = empty endpoints.
