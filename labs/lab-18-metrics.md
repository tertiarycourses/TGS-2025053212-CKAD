# Lab 18 — kubectl top and Metrics

`kubectl top` shows real-time CPU and memory for nodes and Pods, but it needs the **metrics-server** add-on. In this lab you will install metrics-server, watch metrics for a synthetic load Pod, and sort Pods by resource usage.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Install metrics-server

```bash
alias k=kubectl
k apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Killercoda uses self-signed kubelet certs, so patch the Deployment to skip TLS verification:

```bash
k patch -n kube-system deployment metrics-server --type=json -p='
[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
k -n kube-system rollout status deployment/metrics-server
```

Wait until the API is healthy:

```bash
until k top node 2>/dev/null; do echo waiting…; sleep 5; done
```

---

## Step 2 — Top nodes

```bash
k top node
```

---

## Step 3 — Generate load

```bash
k run cpu-burner --image=busybox -- sh -c 'while true; do :; done'
k run idle --image=busybox -- sh -c 'sleep 3600'
sleep 30
```

---

## Step 4 — Top Pods, sorted by CPU

```bash
k top pod
k top pod --sort-by=cpu
k top pod --sort-by=memory
k top pod -A --sort-by=cpu | head
```

The `cpu-burner` Pod should be at the top.

---

## Step 5 — Clean up

```bash
k delete pod cpu-burner idle --force --grace-period 0
```

You can leave metrics-server installed for later labs.

---

## What you learned
- Why `kubectl top` needs metrics-server.
- `--kubelet-insecure-tls` workaround for self-signed kubelet certs.
- `kubectl top node`, `kubectl top pod --sort-by=cpu`.
