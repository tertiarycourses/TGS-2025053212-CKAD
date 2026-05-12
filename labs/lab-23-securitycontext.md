# Lab 23 — SecurityContext

`securityContext` controls who the container runs as, what privileges it has, and what filesystem permissions it gets. CKAD asks you to enforce non-root, read-only filesystem, and dropped capabilities.

Run on the Killercoda Kubernetes Playground:
https://killercoda.com/playgrounds/scenario/kubernetes

---

## Step 1 — Run as a specific UID/GID

```bash
alias k=kubectl
cat > nonroot.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: nonroot }
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
  - name: c
    image: busybox
    command: ["sh","-c","id; touch /tmp/x && ls -ln /tmp/x; sleep 3600"]
EOF
k apply -f nonroot.yaml
sleep 3
k logs nonroot
```

You should see `uid=1000 gid=3000` and the file owned by `1000:3000`.

---

## Step 2 — Enforce runAsNonRoot

```bash
cat > enforce.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: enforced }
spec:
  securityContext:
    runAsNonRoot: true
  containers:
  - name: c
    image: nginx:1.25         # default user is root → will fail
EOF
k apply -f enforce.yaml
sleep 10
k get pod enforced
k describe pod enforced | grep -A1 Reason
```

The Pod will not start: `container has runAsNonRoot and image will run as root`. This is the desired protection.

---

## Step 3 — Read-only root filesystem

```bash
cat > readonly.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: readonly }
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh","-c","touch /root/x 2>&1 || echo as expected; sleep 3600"]
    securityContext:
      readOnlyRootFilesystem: true
EOF
k apply -f readonly.yaml
sleep 3
k logs readonly
```

Writes to `/` fail; mount an `emptyDir` for any path that needs to be writable.

---

## Step 4 — Drop Linux capabilities

```bash
cat > caps.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: { name: caps }
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh","-c","sleep 3600"]
    securityContext:
      capabilities:
        drop: ["ALL"]
        add: ["NET_BIND_SERVICE"]
      allowPrivilegeEscalation: false
EOF
k apply -f caps.yaml
sleep 3
k exec caps -- sh -c 'apk add libcap-utils 2>/dev/null; capsh --print 2>/dev/null || echo capsh missing'
```

A pod-level `securityContext` applies to **all** containers; a container-level block overrides for one container.

---

## Step 5 — Clean up

```bash
k delete pod nonroot enforced readonly caps --force --grace-period 0
```

---

## What you learned
- `runAsUser`, `runAsGroup`, `fsGroup` for identity.
- `runAsNonRoot: true` blocks accidental root containers.
- `readOnlyRootFilesystem` plus capability drops harden a container.
