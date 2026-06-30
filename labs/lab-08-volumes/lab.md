# Lab 8 — Volumes (emptyDir and hostPath)

Containers are ephemeral — any data written to the container filesystem is lost on restart. Volumes survive restarts and can be shared between containers. CKAD 2026 tests `emptyDir`, `emptyDir.medium: Memory`, `hostPath`, and mounting strategies.

Run on https://killercoda.com/playgrounds/scenario/kubernetes

**Required software (free):**
- `kubectl` (pre-installed on Killercoda)
- `busybox` image (pre-pulled on Killercoda)

---

## Step 1 — Set exam aliases

```bash
alias k=kubectl
```

---

## Step 2 — emptyDir shared between two containers

```bash
cat > emptydir.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: scratch
spec:
  volumes:
  - name: shared
    emptyDir: {}
  containers:
  - name: writer
    image: busybox
    command: ["sh", "-c", "echo hello-shared > /data/msg.txt; sleep 3600"]
    volumeMounts:
    - name: shared
      mountPath: /data
  - name: reader
    image: busybox
    command: ["sh", "-c", "sleep 5; cat /data/msg.txt; sleep 3600"]
    volumeMounts:
    - name: shared
      mountPath: /data
EOF
k apply -f scratch.yaml 2>/dev/null || k apply -f emptydir.yaml
sleep 10
k logs scratch -c reader
```

Expected: `hello-shared`. The `emptyDir` is created when the Pod starts and deleted when the Pod is removed.

---

## Step 3 — emptyDir backed by RAM (tmpfs)

```bash
cat > ramdisk.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: ramdisk
spec:
  volumes:
  - name: fast
    emptyDir:
      medium: Memory
      sizeLimit: 64Mi
  containers:
  - name: c
    image: busybox
    command: ["sh", "-c", "df -h /data; sleep 3600"]
    volumeMounts:
    - name: fast
      mountPath: /data
EOF
k apply -f ramdisk.yaml
sleep 3
k logs ramdisk
```

`medium: Memory` mounts a tmpfs — data lives in RAM, is faster, and disappears on Pod termination or node reboot.

---

## Step 4 — hostPath: access files on the node

```bash
cat > hostpath.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: host-peek
spec:
  containers:
  - name: peek
    image: busybox
    command: ["sh", "-c", "ls /node-etc | head -10; sleep 3600"]
    volumeMounts:
    - name: etc
      mountPath: /node-etc
      readOnly: true
  volumes:
  - name: etc
    hostPath:
      path: /etc
      type: Directory
EOF
k apply -f hostpath.yaml
sleep 3
k logs host-peek
```

`hostPath` mounts a directory directly from the underlying node. Only use it for DaemonSets and node-level tools — it is a security risk in multi-tenant clusters.

---

## Step 5 — Clean up

```bash
k delete pod scratch ramdisk host-peek --force --grace-period=0 --ignore-not-found
```

---

## Free online tools

- **Volumes docs**: https://kubernetes.io/docs/concepts/storage/volumes/
- **emptyDir reference**: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `emptyDir: {}` — ephemeral scratch space, shared by all containers in the Pod.
- `emptyDir.medium: Memory` — tmpfs-backed, fast, counted against container memory limits.
- `hostPath` — mounts from the node; avoid in production, useful in DaemonSets.
- Volumes are declared under `spec.volumes` and consumed via `spec.containers[].volumeMounts`.
