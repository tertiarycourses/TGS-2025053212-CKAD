# Step 5: Detect a deprecated API

```bash
cat > old.yaml <<'EOF'
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: legacy
spec: {}
EOF
k apply -f old.yaml --dry-run=client 2>&1 || true
```

`extensions/v1beta1` Ingress was removed in Kubernetes 1.22. The current stable version is `networking.k8s.io/v1`.

---
