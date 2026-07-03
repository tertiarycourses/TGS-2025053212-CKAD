# Step 7: ClusterRole + RoleBinding (one namespace only)

```bash
k create rolebinding dev-node-reader \
  --clusterrole=node-reader \
  --serviceaccount=dev:viewer \
  -n dev
k auth can-i list nodes -n dev --as=system:serviceaccount:dev:viewer
```

A ClusterRole used with a RoleBinding limits permissions to the binding's namespace — a common exam pattern.

---
