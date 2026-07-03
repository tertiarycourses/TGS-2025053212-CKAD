# Step 3: emptyDir backed by RAM (tmpfs)

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
