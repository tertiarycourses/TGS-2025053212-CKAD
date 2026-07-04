# Step 8: Clean up

```bash
k delete pod app --force --grace-period=0
k delete sa app-sa
```

---

## Free online tools

- **ServiceAccount docs**: https://kubernetes.io/docs/concepts/security/service-accounts/
- **Configure ServiceAccounts**: https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- Every Pod runs as a ServiceAccount (`default` if not specified).
- `spec.serviceAccountName` attaches a custom ServiceAccount to a Pod.
- Token, CA cert, and namespace are projected into `/var/run/secrets/kubernetes.io/serviceaccount/`.
- `automountServiceAccountToken: false` enforces least privilege for Pods that don't need API access.
- `kubectl create token <sa>` generates short-lived tokens — the modern replacement for Secret tokens.
