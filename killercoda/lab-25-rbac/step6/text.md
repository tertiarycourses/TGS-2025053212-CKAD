# Step 6: ClusterRole + ClusterRoleBinding (cluster-wide)

```bash
k create clusterrole node-reader --verb=get,list --resource=nodes
k create serviceaccount nodes-sa -n dev
k create clusterrolebinding nodes-binding \
  --clusterrole=node-reader \
  --serviceaccount=dev:nodes-sa
k auth can-i list nodes --as=system:serviceaccount:dev:nodes-sa
```

Expected: `yes`. A ClusterRole bound via ClusterRoleBinding grants permission in all namespaces.

---
