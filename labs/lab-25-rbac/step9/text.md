# Step 9: Clean up

```bash
k delete clusterrolebinding nodes-binding
k delete clusterrole node-reader
k delete namespace dev
```

---

## Free online tools

- **RBAC docs**: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
- **kubectl auth can-i reference**: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_auth_can-i/
- **killer.sh** — CKAD mock exam: https://killer.sh
- **Kubernetes docs** (allowed in CKAD exam): https://kubernetes.io/docs/

---

## What you learned

- `Role` + `RoleBinding` = namespace-scoped permissions.
- `ClusterRole` + `ClusterRoleBinding` = cluster-wide permissions.
- `ClusterRole` + `RoleBinding` = cluster role's verbs limited to one namespace.
- `kubectl auth can-i <verb> <resource> --as=<identity>` validates without authenticating.
