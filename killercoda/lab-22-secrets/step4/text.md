# Step 4: Inject Secret keys as environment variables

```bash
cat > pod-env.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: client
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh", "-c", "echo user=$DB_USER pass=$DB_PASS; sleep 3600"]
    envFrom:
    - secretRef:
        name: db-cred
EOF
k apply -f pod-env.yaml
sleep 3
k logs client
```

---
