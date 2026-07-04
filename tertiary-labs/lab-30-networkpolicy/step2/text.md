# Step 2: Default deny: block all ingress

```bash
cat > deny.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: secured
spec:
  podSelector: {}
  policyTypes:
  - Ingress
EOF
k apply -f deny.yaml
```

`podSelector: {}` matches **all** Pods in the namespace. An empty `ingress:` list means no traffic is allowed in.

```bash
k -n secured exec client-ok -- wget -qO- --timeout=3 backend:5678 || echo "blocked"
```

---
