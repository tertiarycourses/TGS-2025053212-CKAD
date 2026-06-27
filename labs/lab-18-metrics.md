# Lab 18 — kubectl top and Metrics Server

`kubectl top` shows real-time CPU and memory for nodes and Pods. It requires the **metrics-server** add-on. CKAD 2026 tests installation of metrics-server, reading node and Pod metrics, and sorting by resource usage — a common warm-up question in the exam.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `metrics-server` (installed in Step 1)
- `busybox` image (pre-pulled on Killercoda)

---

## Step 1 — Install metrics-server

```bash
alias k=kubectl
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Killercoda uses self-signed kubelet certificates, so patch the Deployment to skip TLS verification:

```bash
kubectl patch -n kube-system deployment metrics-server --type=json -p='
[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
kubectl -n kube-system rollout status deployment/metrics-server
```

Wait for the API to become available:

```bash
until kubectl top node 2>/dev/null; do echo "waiting for metrics..."; sleep 5; done
```

---

## Step 2 — Top nodes

```bash
k top node
```

Shows CPU (cores and %) and memory (bytes and %) per node.

---

## Step 3 — Generate CPU load

```bash
k run cpu-burner --image=busybox -- sh -c 'while true; do :; done'
k run idle --image=busybox -- sh -c 'sleep 3600'
sleep 30
```

Wait 30 seconds for metrics to scrape the new Pods.

---

## Step 4 — Top Pods, sorted by CPU and memory

```bash
k top pod
k top pod --sort-by=cpu
k top pod --sort-by=memory
k top pod -A --sort-by=cpu | head -10
```

`cpu-burner` should appear at the top of the CPU sort. `-A` covers all namespaces.

---

## Step 5 — Top a specific namespace

```bash
k top pod -n kube-system --sort-by=memory
```

---

## Step 6 — Clean up

```bash
k delete pod cpu-burner idle --force --grace-period=0
```

Leave metrics-server installed — it is used in Lab 26 (ResourceQuota).

---

## Free online tools

- **Metrics Server repo**: https://github.com/kubernetes-sigs/metrics-server
- **Resource management docs**: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `kubectl top` requires metrics-server to be installed and running.
- `--kubelet-insecure-tls` is needed on Killercoda due to self-signed certs.
- `kubectl top node` and `kubectl top pod --sort-by=cpu` are exam-day queries.
- `-A` flag covers all namespaces; combine with `| head` to manage output.
