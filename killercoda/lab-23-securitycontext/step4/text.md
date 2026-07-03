# Step 4: Read-only root filesystem

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
