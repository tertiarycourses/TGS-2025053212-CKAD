# Step 4: hostPath: access files on the node

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
