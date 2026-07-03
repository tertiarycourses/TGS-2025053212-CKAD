# Step 3: Selective allow: only role=allowed can reach the backend

```bash
cat > allow.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-role-allowed
  namespace: secured
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: allowed
    ports:
    - protocol: TCP
      port: 5678
EOF
k apply -f allow.yaml
```

```bash
k -n secured exec client-ok  -- wget -qO- --timeout=3 backend:5678
k -n secured exec client-bad -- wget -qO- --timeout=3 backend:5678 || echo "still blocked"
```

`client-ok` succeeds; `client-bad` is still blocked.

---
