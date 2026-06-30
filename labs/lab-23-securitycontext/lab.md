# Lab 23 — SecurityContext

`securityContext` controls the identity and privileges of containers. CKAD 2026 regularly asks you to enforce non-root execution, read-only root filesystem, and dropped Linux capabilities. These fields appear at both Pod level (applies to all containers) and container level (overrides for one container).

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

## Step 2 — Run as a specific user and group

```bash
cat > nonroot.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: nonroot
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
  - name: c
    image: busybox
    command: ["sh", "-c", "id; touch /tmp/x && ls -ln /tmp/x; sleep 3600"]
EOF
k apply -f nonroot.yaml
sleep 3
k logs nonroot
```

Expected: `uid=1000 gid=3000` and the file owned by `1000:2000` (fsGroup applies to volume mounts).

---

## Step 3 — Enforce runAsNonRoot

```bash
cat > enforce.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: enforced
spec:
  securityContext:
    runAsNonRoot: true
  containers:
  - name: c
    image: nginx:1.25
EOF
k apply -f enforce.yaml
sleep 10
k get pod enforced
k describe pod enforced | grep -A2 Reason
```

The Pod will not start — nginx runs as root by default. Error: `container has runAsNonRoot and image will run as root`. This is the intended protection.

---

## Step 4 — Read-only root filesystem

```bash
cat > readonly.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: readonly
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh", "-c", "touch /root/x 2>&1 || echo read-only as expected; sleep 3600"]
    securityContext:
      readOnlyRootFilesystem: true
EOF
k apply -f readonly.yaml
sleep 3
k logs readonly
```

Writes to the container root filesystem are blocked. Mount an `emptyDir` for any path that needs write access (e.g., `/tmp`).

---

## Step 5 — Drop Linux capabilities

```bash
cat > caps.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: caps
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh", "-c", "sleep 3600"]
    securityContext:
      capabilities:
        drop: ["ALL"]
        add: ["NET_BIND_SERVICE"]
      allowPrivilegeEscalation: false
EOF
k apply -f caps.yaml
sleep 3
k exec caps -- sh -c 'cat /proc/1/status | grep Cap'
```

`drop: ["ALL"]` removes every Linux capability. `add` selectively restores only what is needed. `allowPrivilegeEscalation: false` prevents `setuid` binaries from gaining extra privileges.

---

## Step 6 — Clean up

```bash
k delete pod nonroot enforced readonly caps --force --grace-period=0
```

---

## Free online tools

- **SecurityContext docs**: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
- **Linux capabilities reference**: https://man7.org/linux/man-pages/man7/capabilities.7.html
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Pod-level `securityContext` applies to all containers; container-level overrides one.
- `runAsUser`, `runAsGroup`, `fsGroup` — control process and filesystem ownership.
- `runAsNonRoot: true` — blocks any image whose default user is root.
- `readOnlyRootFilesystem: true` + `capabilities.drop: ["ALL"]` + `allowPrivilegeEscalation: false` is the CKAD hardened container pattern.
