# Step 5: Native sidecar container (Kubernetes 1.29+, CKAD 2026)

```bash
cat > native-sidecar.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: native-sidecar-pod
spec:
  initContainers:
  - name: log-collector
    image: busybox
    restartPolicy: Always
    command: ["sh", "-c", "while true; do echo sidecar alive; sleep 5; done"]
  containers:
  - name: main
    image: nginx:1.25
EOF
k apply -f native-sidecar.yaml
sleep 5
k get pod native-sidecar-pod
k logs native-sidecar-pod -c log-collector | head -3
```

A native sidecar is an `initContainer` with `restartPolicy: Always`. It starts before main containers and runs for the Pod's lifetime — it does not block main container startup the way a regular init container does.

---
