# Step 5: Cross-namespace allow (namespaceSelector)

```bash
k create ns trusted
k label ns trusted purpose=trusted

cat > ns-allow.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-trusted-ns
  namespace: secured
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          purpose: trusted
EOF
k apply -f ns-allow.yaml
```

`namespaceSelector` allows all Pods from namespaces matching the label.

---
