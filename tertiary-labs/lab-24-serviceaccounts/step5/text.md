# Step 5: Use the token to call the Kubernetes API

```bash
k exec app -- sh -c '
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
CA=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
curl --cacert $CA -H "Authorization: Bearer $TOKEN" \
  https://kubernetes.default.svc/api/v1/namespaces/default/pods 2>/dev/null | grep -c "kind"'
```

You should see a 403 Forbidden — `app-sa` has no RBAC permissions yet. Lab 25 grants access.

---
