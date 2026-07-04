# Step 4: Egress lockdown: allow DNS only

```bash
cat > egress.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: egress-dns-only
  namespace: secured
spec:
  podSelector:
    matchLabels:
      role: blocked
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
EOF
k apply -f egress.yaml
k -n secured exec client-bad -- wget -qO- --timeout=3 http://example.com || echo "egress blocked"
```

The `client-bad` Pod can still resolve DNS but cannot make outbound TCP connections.

---
