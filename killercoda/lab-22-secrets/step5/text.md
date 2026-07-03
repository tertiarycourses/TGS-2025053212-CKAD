# Step 5: Mount a Secret as files with restrictive permissions

```bash
cat > pod-vol.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: vol
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh", "-c", "ls -l /etc/sec; cat /etc/sec/DB_PASS; sleep 3600"]
    volumeMounts:
    - name: s
      mountPath: /etc/sec
      readOnly: true
  volumes:
  - name: s
    secret:
      secretName: db-cred
      defaultMode: 0400
EOF
k apply -f pod-vol.yaml
sleep 3
k logs vol
k exec vol -- ls -l /etc/sec
```

`defaultMode: 0400` — owner read-only. CKAD frequently asks you to set this.

---
