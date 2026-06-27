# Lab 6 — Multi-Container Pods (Sidecar Pattern)

Containers in the same Pod share a network namespace and can share volumes. CKAD 2026 tests the sidecar pattern (helper reads/writes a shared volume) and the native sidecar container feature (Kubernetes 1.29+). You must be able to exec into a specific container and read logs from each.

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

## Step 2 — Sidecar that tails a shared log file

```bash
cat > sidecar.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: app-with-sidecar
spec:
  volumes:
  - name: logs
    emptyDir: {}
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "i=0; while true; do echo \"$(date) line $i\" >> /var/log/app.log; i=$((i+1)); sleep 2; done"]
    volumeMounts:
    - name: logs
      mountPath: /var/log
  - name: log-shipper
    image: busybox
    command: ["sh", "-c", "tail -F /var/log/app.log"]
    volumeMounts:
    - name: logs
      mountPath: /var/log
EOF
k apply -f sidecar.yaml
k get pod app-with-sidecar
```

The shared `emptyDir` is the glue: `app` writes, `log-shipper` reads — both see `/var/log`.

---

## Step 3 — Read logs from each container separately

```bash
k logs app-with-sidecar -c app | head -5
k logs app-with-sidecar -c log-shipper | head -5
k logs app-with-sidecar --all-containers=true --prefix=true | head -10
```

`-c <name>` selects the container. On exam: when a Pod has multiple containers, always specify `-c`.

---

## Step 4 — Exec into a specific container

```bash
k exec -it app-with-sidecar -c app -- sh -c 'ls /var/log; wc -l /var/log/app.log'
```

---

## Step 5 — Native sidecar container (Kubernetes 1.29+, CKAD 2026)

```bash
cat > native-sidecar.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: native-sidecar-pod
spec:
  initContainers:
  - name: log-collector
    image: busybox
    restartPolicy: Always
    command: ["sh", "-c", "while true; do echo sidecar alive; sleep 5; done"]
  containers:
  - name: main
    image: nginx:1.25
EOF
k apply -f native-sidecar.yaml
sleep 5
k get pod native-sidecar-pod
k logs native-sidecar-pod -c log-collector | head -3
```

A native sidecar is an `initContainer` with `restartPolicy: Always`. It starts before main containers and runs for the Pod's lifetime — it does not block main container startup the way a regular init container does.

---

## Step 6 — Clean up

```bash
k delete pod app-with-sidecar native-sidecar-pod --force --grace-period=0
```

---

## Free online tools

- **Sidecar pattern docs**: https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/
- **Multi-container Pod docs**: https://kubernetes.io/docs/concepts/workloads/pods/#how-pods-manage-multiple-containers
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Containers in the same Pod share the network namespace and optionally volumes.
- `kubectl logs -c <container>` and `kubectl exec -c <container>` for multi-container Pods.
- Native sidecars (Kubernetes 1.29+): `initContainer` with `restartPolicy: Always`.
- `emptyDir` is the standard glue volume between sidecar and main containers.
