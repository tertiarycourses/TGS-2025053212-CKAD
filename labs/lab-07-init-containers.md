# Lab 7 — Init Containers

Init containers run **in order, to completion**, before any main container starts. Use them to seed shared volumes, wait for upstream services, or do one-time setup. CKAD 2026 asks you to write init containers from scratch and read `Init:N/M` Pod status correctly.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `busybox`, `nginx:1.25` images (pulled automatically)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
```

---

## Step 2 — Init container that seeds the web root

```bash
cat > init.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: web-init
spec:
  volumes:
  - name: html
    emptyDir: {}
  initContainers:
  - name: seed
    image: busybox
    command: ["sh", "-c", "echo '<h1>Seeded by init container</h1>' > /work/index.html"]
    volumeMounts:
    - name: html
      mountPath: /work
  containers:
  - name: web
    image: nginx:1.25
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
EOF
k apply -f init.yaml
k get pod web-init
```

While the init container runs you see `Init:0/1`. After it exits 0, the main container starts and status becomes `Running`.

---

## Step 3 — Verify the seeded content

```bash
k exec web-init -- cat /usr/share/nginx/html/index.html
```

Expected: `<h1>Seeded by init container</h1>`

---

## Step 4 — Init container that waits for a Service

```bash
cat > wait.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: app-waiting
spec:
  initContainers:
  - name: wait-for-db
    image: busybox
    command: ["sh", "-c", "until nslookup db.default.svc.cluster.local; do echo waiting for db; sleep 2; done"]
  containers:
  - name: app
    image: nginx:1.25
EOF
k apply -f wait.yaml
k get pod app-waiting
k logs app-waiting -c wait-for-db | head -5
```

The Pod stays in `Init:0/1` until DNS resolves. This is a blocking readiness gate.

---

## Step 5 — Unblock the init container by creating the Service

```bash
k create service clusterip db --tcp=5432:5432
k get pod app-waiting -w
```

Once CoreDNS can resolve `db.default.svc.cluster.local`, the init container exits and the main container starts. Press Ctrl+C after status shows `Running`.

---

## Step 6 — Clean up

```bash
k delete pod web-init app-waiting --force --grace-period=0
k delete service db
```

---

## Free online tools

- **Init containers docs**: https://kubernetes.io/docs/concepts/workloads/pods/init-containers/
- **Pod lifecycle reference**: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Init containers run sequentially before any main container starts.
- Pod status `Init:N/M` means N of M init containers have completed.
- Common use cases: seed volumes, wait for DNS/service, one-time DB migration.
- If an init container fails, Kubernetes restarts it according to the Pod's `restartPolicy`.
