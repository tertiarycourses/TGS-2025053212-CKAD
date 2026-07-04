# Step 2: emptyDir shared between two containers

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
