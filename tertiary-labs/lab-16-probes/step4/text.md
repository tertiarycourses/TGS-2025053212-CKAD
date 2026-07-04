# Step 4: TCP socket probe

```bash
cat > tcp-probe.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: db-probe
spec:
  containers:
  - name: db
    image: redis:7
    ports:
    - containerPort: 6379
    readinessProbe:
      tcpSocket:
        port: 6379
      periodSeconds: 5
EOF
k apply -f tcp-probe.yaml
k get pod db-probe
```

A TCP probe succeeds when the TCP handshake completes — no HTTP server required.

---
