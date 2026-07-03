# Step 2: Run as a specific user and group

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
