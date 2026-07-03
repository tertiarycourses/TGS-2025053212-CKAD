# Step 3: Enforce runAsNonRoot

```bash
cat > enforce.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: enforced
spec:
  securityContext:
    runAsNonRoot: true
  containers:
  - name: c
    image: nginx:1.25
EOF
k apply -f enforce.yaml
sleep 10
k get pod enforced
k describe pod enforced | grep -A2 Reason
```

The Pod will not start — nginx runs as root by default. Error: `container has runAsNonRoot and image will run as root`. This is the intended protection.

---
