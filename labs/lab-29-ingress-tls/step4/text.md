# Step 4: Create the Ingress with TLS and host routing

```bash
cat > ing.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: demo
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - demo.local
    secretName: demo-tls
  rules:
  - host: demo.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web
            port:
              number: 5678
EOF
k apply -f ing.yaml
k get ing demo
```

Key fields: `ingressClassName: nginx` (selects the controller), `tls.secretName` (points at your TLS Secret), `pathType: Prefix` (matches `/` and anything below).

---
