# Lab 8 — Volumes (emptyDir and hostPath)

Containers are ephemeral; volumes are how data survives a restart or is shared between containers in a Pod. In this lab you will mount an `emptyDir` for inter-container scratch space and a `hostPath` for direct node access. PersistentVolumes are covered later in the deployment domain.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — emptyDir shared between two containers

```bash
alias k=kubectl
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
    command: ["sh","-c","echo hello-shared > /data/msg.txt; sleep 3600"]
    volumeMounts:
    - { name: shared, mountPath: /data }
  - name: reader
    image: busybox
    command: ["sh","-c","sleep 5; cat /data/msg.txt; sleep 3600"]
    volumeMounts:
    - { name: shared, mountPath: /data }
EOF
k apply -f emptydir.yaml
sleep 8
k logs scratch -c reader
```

`emptyDir` lives as long as the Pod. Deleting the Pod erases it.

---

## Step 2 — emptyDir backed by RAM

```bash
k delete pod scratch --force --grace-period 0
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
    command: ["sh","-c","mount | grep /data; sleep 3600"]
    volumeMounts:
    - { name: fast, mountPath: /data }
EOF
k apply -f ramdisk.yaml
sleep 3
k logs ramdisk
```

`medium: Memory` allocates a tmpfs — handy for cache or secrets.

---

## Step 3 — hostPath: see files on the underlying node

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
    command: ["sh","-c","ls /node-etc | head; sleep 3600"]
    volumeMounts:
    - { name: etc, mountPath: /node-etc, readOnly: true }
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

`hostPath` mounts a path **from the node** into the Pod. Treat it as a security risk in production — used here only for learning.

---

## Step 4 — Clean up

```bash
k delete pod ramdisk host-peek --force --grace-period 0
```

---

## What you learned
- `emptyDir` for ephemeral Pod-local scratch space.
- `emptyDir.medium: Memory` for tmpfs-backed fast storage.
- `hostPath` for direct node access — useful in DaemonSets, risky elsewhere.
