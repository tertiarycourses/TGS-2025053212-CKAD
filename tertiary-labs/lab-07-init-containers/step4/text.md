# Step 4: Init container that waits for a Service

```bash
cat > wait.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: app-waiting
spec:
  initContainers:
  - name: wait-for-db
    image: busybox
    command: ["sh", "-c", "until nslookup db.default.svc.cluster.local; do echo waiting for db; sleep 2; done"]
  containers:
  - name: app
    image: nginx:1.25
EOF
k apply -f wait.yaml
k get pod app-waiting
k logs app-waiting -c wait-for-db | head -5
```

The Pod stays in `Init:0/1` until DNS resolves. This is a blocking readiness gate.

---
