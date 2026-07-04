# Step 4: Inject all keys with envFrom

```bash
cat > pod-bulk.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: bulk
spec:
  containers:
  - name: c
    image: busybox
    command: ["sh", "-c", "env | grep -E 'COLOR|GREETING|TIMEOUT|RETRIES'; sleep 3600"]
    envFrom:
    - configMapRef:
        name: app-cfg
    - configMapRef:
        name: app-env
EOF
k apply -f pod-bulk.yaml
sleep 3
k logs bulk
```

`envFrom` loads every key in the ConfigMap as an environment variable — no need to name them individually.

---
